from django.db import transaction
from .models import Category, Product, UnitOfMeasure

@transaction.atomic
def category_create(*, name: str, **extra_fields) -> Category:
    return Category.objects.create(name=name, **extra_fields)

@transaction.atomic
def category_update(*, category: Category, data: dict) -> Category:
    for field, value in data.items():
        setattr(category, field, value)
    category.save()
    return category

@transaction.atomic
def category_delete(*, category: Category):
    category.is_active = False
    category.save()

@transaction.atomic
def product_create(
    *, 
    name: str, 
    quantity: float, 
    unit_of_measure: UnitOfMeasure,
    description: str = "", 
    image=None,
    **extra_fields
) -> Product:
    categories = extra_fields.pop('categories', None)
    
    product = Product.objects.create(
        name=name,
        quantity=quantity,
        unit_of_measure=unit_of_measure,
        description=description,
        image=image,
        **extra_fields
    )
    
    if categories:
        product.categories.set(categories)
        
    return product

@transaction.atomic
def product_update(*, product: Product, data: dict) -> Product:
    categories = data.pop('categories', None)
    
    for field, value in data.items():
        setattr(product, field, value)
    
    if categories is not None:
        product.categories.set(categories)
        
    product.save()
    return product

@transaction.atomic
def product_delete(*, product: Product):
    product.is_active = False
    product.save()
