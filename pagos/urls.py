# pagos/urls.py

from django.urls import path
from . import views

app_name = 'pagos'

urlpatterns = [
    # URLs para la interfaz de usuario (el formulario y la página de estado)
    path('', views.seleccionar_metodo, name='seleccionar_metodo'),
    path('transferencia/', views.transferencia, name='transferencia'),
    path('billetera/', views.billetera, name='billetera'),

    # URLs para la API (si las necesitas después)
    path('api/crear-pago/', views.crear_pago, name='crear_pago'),
    path('api/estado/<str:id_transaccion>/', views.obtener_estado, name='obtener_estado'),

    # URLs actualizadas
    path('crear/', views.crear_pago, name='crear_pago'),
    path('estado/<str:id_transaccion>/', views.obtener_estado, name='obtener_estado'),
    path('estado-pago/<str:id_transaccion>/', views.estado_pago, name='estado_pago'),

    # Nuevas URLs para la API
    path('api/transaccion/<str:codigo_operacion>/', views.consultar_transaccion, name='consultar_transaccion'),
    path('api/transaccion/<str:codigo_operacion>/actualizar/', views.actualizar_estado, name='actualizar_estado'),
]