from django.contrib import admin
from .models import PaymentMethod, Currency, PaymentType

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'symbol', 'is_active')
    search_fields = ('name', 'code')

@admin.register(PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name',)

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'payment_type', 'currency', 'is_active', 'created_at')
    list_filter = ('payment_type', 'currency', 'is_active')
    search_fields = ('name', 'details')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'payment_type', 'currency', 'is_active')
        }),
        ('Detalles y Multimedia', {
            'fields': ('details', 'image')
        }),
        ('Fechas de Auditoría', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
        }),
    )
