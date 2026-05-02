from django.db.models import QuerySet
from .models import PaymentMethod, Currency, PaymentType

def currency_list() -> QuerySet:
    return Currency.objects.filter(is_active=True)

def payment_type_list() -> QuerySet:
    return PaymentType.objects.filter(is_active=True)

def payment_method_list(*, include_inactive: bool = False) -> QuerySet:
    queryset = PaymentMethod.objects.select_related('payment_type', 'currency').all()
    if not include_inactive:
        queryset = queryset.filter(is_active=True)
    return queryset
