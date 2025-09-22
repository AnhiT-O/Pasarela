# pagos/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
import uuid
from .models import Transaccion

@csrf_exempt
def crear_pago(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            monto = data.get('monto')
            metodo = data.get('metodo_pago')
            referencia = data.get('referencia_pago')

            # Generar un ID único para la transacción
            id_externo = str(uuid.uuid4())

            # Crear la transacción simulada
            transaccion = Transaccion.objects.create(
                id_externo=id_externo,
                monto=monto,
                metodo_pago=metodo,
                referencia_pago=referencia
            )
            return JsonResponse({
                'status': 'pendiente', 
                'id_transaccion': id_externo,
                'monto': str(transaccion.monto),
                'metodo': transaccion.metodo_pago
            })
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return render(request, 'pagos/formulario_pago.html')

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
# Create your views here.
    return render(request, 'pagos/billetera.html')
# Create your views here.
