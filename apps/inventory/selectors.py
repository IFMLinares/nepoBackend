from django.db.models import QuerySet
from .models import Category, Product, UnitOfMeasure

def category_list() -> QuerySet:
    return Category.objects.filter(is_active=True)

def unit_of_measure_list() -> QuerySet:
    return UnitOfMeasure.objects.filter(is_active=True)

def product_list(*, include_inactive: bool = False) -> QuerySet:
    queryset = Product.objects.select_related('unit_of_measure').prefetch_related('categories').all()
    if not include_inactive:
        queryset = queryset.filter(is_active=True)
    return queryset
