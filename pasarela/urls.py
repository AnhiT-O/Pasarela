# pasarela/urls.py

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def redirect_to_pagos(request):
    return redirect('pagos:crear_pago')

urlpatterns = [
    path('', redirect_to_pagos, name='home'),
    path('admin/', admin.site.urls),
    path('pagos/', include('pagos.urls', namespace='pagos')),
]