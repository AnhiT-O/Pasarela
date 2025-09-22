# pagos/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
import uuid
import random
import string
from .models import Transaccion

@csrf_exempt
def crear_pago(request):
    if request.method == 'GET':
        return render(request, 'pagos/formulario_pago.html')
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            monto = data.get('monto')
            metodo = data.get('metodo_pago')
            referencia = data.get('referencia_pago')

            # Generar un ID único para la transacción
            id_externo = str(uuid.uuid4())

            # Generar un código de operación único (ejemplo: 8 caracteres alfanuméricos)
            codigo_operacion = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

            # Agregar URL del webhook si viene en la petición
            webhook_url = data.get('webhook_url')
            webhook_secret = data.get('webhook_secret')
            
            # Crear la transacción simulada
            transaccion = Transaccion.objects.create(
                id_externo=id_externo,
                monto=monto,
                metodo_pago=metodo,
                referencia_pago=referencia,
                codigo_operacion=codigo_operacion,
                webhook_url=webhook_url,
                webhook_secret=webhook_secret
            )
            return JsonResponse({
                'status': 'pendiente', 
                'id_transaccion': id_externo,
                'codigo_operacion': codigo_operacion,
                'monto': str(transaccion.monto),
                'metodo': transaccion.metodo_pago
            })
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def obtener_estado(request, id_transaccion):
    try:
        transaccion = Transaccion.objects.get(id_externo=id_transaccion)
        return JsonResponse({
            'status': transaccion.estado,
            'monto': str(transaccion.monto),
            'metodo_pago': transaccion.metodo_pago,
            'referencia': transaccion.referencia_pago,
            'id_transaccion': transaccion.id_externo
        })
    except Transaccion.DoesNotExist:
        return JsonResponse({'error': 'Transacción no encontrada'}, status=404)

def formulario_pago(request):
    return render(request, 'pagos/formulario_pago.html')

def estado_pago(request, id_transaccion):
    try:
        transaccion = Transaccion.objects.get(id_externo=id_transaccion)
        context = {
            'transaccion': transaccion,
            'estado_actual': transaccion.estado
        }
        template_name = 'pagos/estado_pago.html'
        return render(request, template_name, context)
    except Transaccion.DoesNotExist:
        return JsonResponse({
            'error': 'Transacción no encontrada'
        }, status=404)

def seleccionar_metodo(request):
    return render(request, 'pagos/formulario_pago.html')

def transferencia(request):
    return render(request, 'pagos/transferencia.html')

def billetera(request):
    return render(request, 'pagos/billetera.html')

@csrf_exempt
def consultar_transaccion(request, codigo_operacion):
    """
    Endpoint para que sistemas externos consulten una transacción
    """
    try:
        transaccion = Transaccion.objects.get(codigo_operacion=codigo_operacion)
        return JsonResponse({
            'codigo_operacion': transaccion.codigo_operacion,
            'estado': transaccion.estado,
            'monto': str(transaccion.monto),
            'metodo_pago': transaccion.metodo_pago,
            'fecha_creacion': transaccion.fecha_creacion.isoformat()
        })
    except Transaccion.DoesNotExist:
        return JsonResponse({'error': 'Transacción no encontrada'}, status=404)

@csrf_exempt
def actualizar_estado(request, codigo_operacion):
    """
    Endpoint para que sistemas externos actualicen el estado de una transacción
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    try:
        data = json.loads(request.body)
        nuevo_estado = data.get('estado')
        
        transaccion = Transaccion.objects.get(codigo_operacion=codigo_operacion)
        transaccion.estado = nuevo_estado
        transaccion.save()
        
        # Enviar webhook
        transaccion.notificar_cambio_estado()
        
        return JsonResponse({
            'codigo_operacion': transaccion.codigo_operacion,
            'estado': transaccion.estado,
            'mensaje': 'Estado actualizado correctamente'
        })
    except Transaccion.DoesNotExist:
        return JsonResponse({'error': 'Transacción no encontrada'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
