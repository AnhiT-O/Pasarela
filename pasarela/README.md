# Pasarela de Pagos - Guía de Integración

## Configuración en el Proyecto Cliente

1. Instalar dependencias necesarias:
```python
pip install requests
```

2. Agregar las siguientes variables en tu settings.py:
```python
PASARELA_URL = 'http://tu-dominio.com'  # URL base de la pasarela
PASARELA_SECRET = 'tu_clave_secreta'    # Clave para firmar webhooks
```

3. Crear un modelo para registrar las transacciones:
```python
from django.db import models

class TransaccionPago(models.Model):
    codigo_operacion = models.CharField(max_length=20, unique=True)
    estado = models.CharField(max_length=20)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
```

4. Crear una vista para recibir webhooks:
```python
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import hmac
import hashlib
import json

@csrf_exempt
def webhook_handler(request):
    if request.method == 'POST':
        # Verificar firma
        signature = request.headers.get('X-Signature')
        if signature:
            expected_signature = hmac.new(
                settings.PASARELA_SECRET.encode(),
                request.body,
                hashlib.sha256
            ).hexdigest()
            
            if signature != expected_signature:
                return JsonResponse({'error': 'Firma inválida'}, status=400)
        
        try:
            data = json.loads(request.body)
            TransaccionPago.objects.update_or_create(
                codigo_operacion=data['codigo_operacion'],
                defaults={
                    'estado': data['estado'],
                    'monto': data['monto']
                }
            )
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)
```

5. Agregar la URL del webhook:
```python
from django.urls import path
from . import views

urlpatterns = [
    path('webhooks/pagos/', views.webhook_handler, name='webhook_pagos'),
]
```

## Uso de la API

### 1. Crear un nuevo pago

```python
import requests

def crear_pago(monto, metodo_pago, referencia):
    response = requests.post(
        f'{settings.PASARELA_URL}/pagos/crear/',
        json={
            'monto': monto,
            'metodo_pago': metodo_pago,
            'referencia_pago': referencia,
            'webhook_url': 'https://tu-dominio.com/webhooks/pagos/',
            'webhook_secret': settings.PASARELA_SECRET
        }
    )
    return response.json()
```

### 2. Consultar estado de un pago

```python
def consultar_pago(codigo_operacion):
    response = requests.get(
        f'{settings.PASARELA_URL}/pagos/api/transaccion/{codigo_operacion}/'
    )
    return response.json()
```

### 3. Actualizar estado manualmente

```python
def actualizar_estado(codigo_operacion, nuevo_estado):
    response = requests.post(
        f'{settings.PASARELA_URL}/pagos/api/transaccion/{codigo_operacion}/actualizar/',
        json={'estado': nuevo_estado}
    )
    return response.json()
```

## Eventos Webhook

La pasarela enviará actualizaciones a tu webhook en los siguientes casos:

- Cuando se crea un nuevo pago
- Cuando cambia el estado de un pago
- Cuando se completa o falla una transacción

El payload del webhook incluirá:
```json
{
    "codigo_operacion": "ABC123",
    "estado": "COMPLETADO",
    "monto": "150000.00",
    "metodo_pago": "TRANSFERENCIA",
    "fecha_actualizacion": "2024-01-20T15:30:00Z"
}
```

## Estados Posibles

- `PENDIENTE`: Pago iniciado pero no confirmado
- `COMPLETADO`: Pago confirmado exitosamente
- `FALLIDO`: Pago rechazado o fallido

## Seguridad

1. Todas las peticiones webhook incluyen una firma en el header `X-Signature`
2. Verifica siempre la firma usando tu `PASARELA_SECRET`
3. Usa HTTPS en producción
4. Mantén tu `PASARELA_SECRET` seguro

## Manejo de Errores

- 400: Datos inválidos o error de validación
- 401: Error de autenticación
- 404: Recurso no encontrado
- 500: Error interno del servidor

## Soporte

Para ayuda adicional, contacta a soporte@tupasarela.com
