from django.db.models import QuerySet
from .models import PaymentMethod

def payment_method_list(*, include_inactive: bool = False) -> QuerySet:
    queryset = PaymentMethod.objects.all()
    if not include_inactive:
        queryset = queryset.filter(is_active=True)
    return queryset
