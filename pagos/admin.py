# pagos/admin.py
# pagos/admin.py

from django.contrib import admin
from .models import Transaccion

# Acciones personalizadas para el panel de administración
def confirmar_pago(modeladmin, request, queryset):
    queryset.update(estado='CONFIRMADO')
confirmar_pago.short_description = "Confirmar pagos seleccionados"

def rechazar_pago(modeladmin, request, queryset):
    queryset.update(estado='RECHAZADO')
rechazar_pago.short_description = "Rechazar pagos seleccionados"

@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):  # Nombre de clase corregido
    list_display = (
        'id',
        'monto',
        'metodo_pago',
        'referencia_pago',
        'estado',
        'fecha_creacion'
    )
    list_filter = ('estado', 'metodo_pago')
    # Quita 'usuario__username' ya que el modelo no tiene ese campo
    search_fields = ('referencia_pago',)
    actions = [confirmar_pago, rechazar_pago]