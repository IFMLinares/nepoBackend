from django.db import models
from apps.common.models import TimestampedModel

class Currency(TimestampedModel):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10, unique=True)
    symbol = models.CharField(max_length=5)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        verbose_name = "Moneda"
        verbose_name_plural = "Monedas"

class PaymentType(TimestampedModel):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tipo de Pago"
        verbose_name_plural = "Tipos de Pago"

class PaymentMethod(TimestampedModel):
    name = models.CharField(max_length=100)
    payment_type = models.ForeignKey(
        PaymentType, 
        on_delete=models.PROTECT, 
        related_name='payment_methods'
    )
    currency = models.ForeignKey(
        Currency, 
        on_delete=models.PROTECT, 
        related_name='payment_methods'
    )
    details = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='payment_methods/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.currency.code if self.currency else ''} ({self.payment_type.name if self.payment_type else ''})"

    class Meta:
        ordering = ['name']
        verbose_name = "Método de Pago"
        verbose_name_plural = "Métodos de Pago"
