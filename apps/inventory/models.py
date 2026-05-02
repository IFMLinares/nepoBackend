from django.db import models
from apps.common.models import TimestampedModel

class Category(TimestampedModel):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['name']

class UnitOfMeasure(TimestampedModel):
    name = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.abbreviation})"

    class Meta:
        verbose_name = "Unidad de Medida"
        verbose_name_plural = "Unidades de Medida"

class Product(TimestampedModel):
    name = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='inventory/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    unit_of_measure = models.ForeignKey(
        UnitOfMeasure, 
        on_delete=models.PROTECT, 
        related_name='products'
    )
    categories = models.ManyToManyField(
        Category, 
        related_name='products'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['name']
