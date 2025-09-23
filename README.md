# Pasarela de Pagos - Guía de Integración

## Configuración del Proyecto de Compra/Venta
Para permitir la comunicación entre la pasarela y el proyecto principal, es necesario configurar CORS:

### 1. Instalar django-cors-headers
```bash
pip install django-cors-headers
```

### 2. Configurar Vista en Django (proyecto de compra/venta)

En views.py:
```python
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def recibir_pago(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            estado = data.get('estado')       # 'exito', 'error' o 'cancelado'
            monto = data.get('monto')
            
            # Datos específicos según el tipo de pago
            tipo_pago = data.get('tipo_pago')  # Para billetera móvil
            banco = data.get('banco')          # Para transferencia
            usuario = data.get('usuario')      # CI o RUC del usuario
            
            # Validar datos requeridos
            if estado not in ['exito', 'error', 'cancelado']:
                return JsonResponse({'status': 'error', 'mensaje': 'Estado inválido'})
                
            if estado != 'cancelado' and not monto:
                return JsonResponse({'status': 'error', 'mensaje': 'Monto requerido'})

            # Aquí procesas los datos según necesites
            print("Pago recibido:", data)

            return JsonResponse({'status': 'ok'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'mensaje': 'JSON inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'mensaje': str(e)}, status=500)
    return JsonResponse({'status': 'método no permitido'}, status=405)
```

En urls.py:
```python
from django.urls import path
from . import views

urlpatterns = [
    path('recibir_pago/', views.recibir_pago, name='recibir_pago'),
]
```

### 3. Configurar CORS en settings.py
```python
INSTALLED_APPS = [
    ...,
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5500",  # URL donde se sirve tu HTML de pasarela
]
```
Ajusta el puerto según dónde estés sirviendo tu HTML de la pasarela.

## Conexión con Proyecto de Compra/Venta
Esta pasarela se integra con el proyecto de compra/venta disponible en:
https://github.com/AnhiT-O/proyectoIS

Para desarrollo local:
1. Clona y ejecuta el proyecto de compra/venta en localhost:8000
2. La pasarela enviará las notificaciones automáticamente a la API de pagos

## Configuración de los Proyectos

### Repositorios
- Pasarela de Pagos: https://github.com/AnhiT-O/Pasarela
- Proyecto de Compra/Venta: https://github.com/AnhiT-O/proyectoIS

### Pasos para la Integración
1. Clona ambos repositorios
2. Configura CORS en el proyecto de compra/venta (como se indica arriba)
3. En el proyecto de compra/venta, configura las redirecciones:

```python
# Para billetera móvil
window.location.href = 'http://localhost:5500/pagos/templates/pagos/billetera.html'

# Para transferencia bancaria
window.location.href = 'http://localhost:5500/pagos/templates/pagos/transferencia.html'
```

### Ejemplo de Implementación en el Proyecto Principal

```html
<!-- En tu formulario de selección de pago -->
<script>
function redirigirAPago(metodoPago) {
    const BASE_URL = 'http://localhost:5500/pagos/templates/pagos/';
    
    if (metodoPago === 'billetera') {
        window.location.href = BASE_URL + 'billetera.html';
    } else if (metodoPago === 'transferencia') {
        window.location.href = BASE_URL + 'transferencia.html';
    }
}
</script>

<button onclick="redirigirAPago('billetera')">Pagar con Billetera</button>
<button onclick="redirigirAPago('transferencia')">Pagar con Transferencia</button>
```

### Recepción de Notificaciones
La pasarela notificará automáticamente al endpoint `/recibir_pago/` del proyecto principal.

## Estados del Pago

La pasarela notificará al proyecto principal sobre el estado del pago:

- `exito`: El pago se completó exitosamente
- `error`: Hubo un error en el pago o los datos no son válidos
- `cancelado`: El usuario abandonó el proceso de pago

## Notificaciones al Proyecto Principal

La pasarela enviará automáticamente los resultados del pago a la API del proyecto principal:

```javascript
// Ejemplo del formato de datos enviados
{
    "estado": "exito", // o "error" o "cancelado"
    "monto": "150000.00", // solo en caso de éxito o error
    "tipo_pago": "TIGO", // o banco en caso de transferencia
    "usuario": "1234567" // número de documento del usuario
}
```

## API Endpoint

La pasarela enviará las notificaciones a:
```
http://localhost:8000/api/pago/  # Ajusta esta URL según tu configuración
```
## 📌 Desglosemos la URL:

http://localhost:8000
→ es la dirección de tu servidor Django.

localhost significa que corre en tu computadora local.

8000 es el puerto que usa Django por defecto (python manage.py runserver).

/api/pago/
→ es la ruta del endpoint que defines en tu urls.py para manejar los pagos.

Puede llamarse /api/pago/, /pagos/recibir/, /transacciones/, o como quieras.

Lo importante es que coincida con la vista en Django que escribiste (recibir_pago).


## Seguridad

1. Usa HTTPS en producción
2. Asegura que la URL de tu API esté correctamente configurada

# Pasarela de Pagos

## Base de Datos de Prueba - Billeteras Móviles

| Tipo Billetera | Teléfono   | CI      |
|----------------|------------|---------|
| TIGO           | 0981000001 | 1010101 |
| PERSONAL       | 0982000002 | 2020202 |
| ZIMPLE         | 0983000003 | 3030303 |
| TIGO           | 0984000004 | 4040404 |
| PERSONAL       | 0985000005 | 5050505 |
| ZIMPLE         | 0986000006 | 6060606 |
| TIGO           | 0987000007 | 7070707 |
| PERSONAL       | 0988000008 | 8080808 |
| ZIMPLE         | 0989000009 | 9090909 |
| TIGO           | 0981010100 | 1111111 |

## Base de Datos de Prueba - Cuentas Bancarias

| Banco   | Nro. Cuenta | Titular           | Tipo Doc | Nro. Documento | Tipo Cuenta |
|---------|-------------|-------------------|----------|----------------|-------------|
| BBVA    | 123456      | Global Exchange   | RUC      | 1234567        | Empresa     |
| ITAU    | 987654      | Juan Pérez       | CI       | 4567890        | Personal    |
| BNF     | 555888      | María López      | CI       | 1122334        | Personal    |
| VISION  | 777999      | Empresa XYZ      | RUC      | 8899001        | Empresa     |
| GNB     | 111222      | Carlos Fernández | CI       | 2233445        | Personal    |
| ITAU    | 333444      | Ana Gómez        | CI       | 3344556        | Personal    |
| BBVA    | 555666      | Empresa ABC      | RUC      | 4455667        | Empresa     |
| BNF     | 777888      | Pedro Martínez   | CI       | 5566778        | Personal    |
| VISION  | 999000      | Empresa LMN      | RUC      | 6677889        | Empresa     |
| GNB     | 222333      | Lucía Ramírez    | CI       | 7788990        | Personal    |
