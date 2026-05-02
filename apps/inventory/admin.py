from django.contrib import admin
from .models import Category, Product, UnitOfMeasure

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    search_fields = ('name',)
    list_filter = ('is_active',)

@admin.register(UnitOfMeasure)
class UnitOfMeasureAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation', 'is_active')
    search_fields = ('name', 'abbreviation')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'unit_of_measure', 'is_active')
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'categories', 'unit_of_measure')
    filter_horizontal = ('categories',)
