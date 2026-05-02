from django.db import transaction
from .models import PaymentMethod, Currency, PaymentType

@transaction.atomic
def payment_method_create(
    *, 
    name: str, 
    payment_type: PaymentType, 
    currency: Currency, 
    details: str = None, 
    image=None, 
    **extra_fields
) -> PaymentMethod:
    return PaymentMethod.objects.create(
        name=name,
        payment_type=payment_type,
        currency=currency,
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
    payment_method.is_active = False
    payment_method.save()
