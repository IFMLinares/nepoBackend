from django.db import transaction
from .models import PaymentMethod

@transaction.atomic
def payment_method_create(*, name: str, method_type: str, details: str = None, image=None, **extra_fields) -> PaymentMethod:
    return PaymentMethod.objects.create(
        name=name,
        method_type=method_type,
        details=details,
        image=image,
        **extra_fields
    )

@transaction.atomic
def payment_method_update(*, payment_method: PaymentMethod, data: dict) -> PaymentMethod:
    for field, value in data.items():
        setattr(payment_method, field, value)
    
    payment_method.full_clean()
    payment_method.save()
    return payment_method

@transaction.atomic
def payment_method_delete(*, payment_method: PaymentMethod):
    # TODO: Validar que no haya transacciones vinculadas antes de desactivar
    payment_method.is_active = False
    payment_method.save()
