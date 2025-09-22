# pagos/models.py
from django.db import models

class Transaccion(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('COMPLETADO', 'Completado'),
        ('FALLIDO', 'Fallido'),
    ]

    id_externo = models.CharField(max_length=100, unique=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=50)
    referencia_pago = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    codigo_operacion = models.CharField(max_length=10, unique=True)
    webhook_url = models.URLField(blank=True, null=True)
    webhook_secret = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return f"Transacción {self.id_externo} - {self.estado}"

    def notificar_cambio_estado(self):
        if self.webhook_url:
            try:
                import requests
                import hmac
                import hashlib
                
                payload = {
                    'codigo_operacion': self.codigo_operacion,
                    'estado': self.estado,
                    'monto': str(self.monto),
                    'metodo_pago': self.metodo_pago,
                    'fecha_actualizacion': self.fecha_creacion.isoformat()
                }
                
                # Generar firma para seguridad
                if self.webhook_secret:
                    signature = hmac.new(
                        self.webhook_secret.encode(),
                        str(payload).encode(),
                        hashlib.sha256
                    ).hexdigest()
                    headers = {'X-Signature': signature}
                else:
                    headers = {}
                
                # Enviar notificación al otro sistema
                requests.post(
                    self.webhook_url,
                    json=payload,
                    headers=headers,
                    timeout=5
                )
            except Exception as e:
                print(f"Error al notificar webhook: {e}")