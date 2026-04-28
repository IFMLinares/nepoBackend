from django.db import models
from apps.common.models import TimestampedModel

class PaymentMethod(TimestampedModel):
    class MethodType(models.TextChoices):
        CARD = 'CARD', 'Tarjeta de Crédito/Débito'
        CASH = 'CASH', 'Efectivo'
        TRANSFER = 'TRANSFER', 'Transferencia/Pago Móvil'

    name = models.CharField(max_length=100)
    method_type = models.CharField(
        max_length=20, 
        choices=MethodType.choices, 
        default=MethodType.CASH
    )
    details = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='payment_methods/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.get_method_type_display()})"

    class Meta:
        ordering = ['name']
