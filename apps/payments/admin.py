from django.contrib import admin
from .models import PaymentMethod

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'method_type', 'is_active', 'created_at')
    list_filter = ('method_type', 'is_active')
    search_fields = ('name', 'details')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'method_type', 'is_active')
        }),
        ('Detalles y Multimedia', {
            'fields': ('details', 'image')
        }),
        ('Fechas de Auditoría', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
        }),
    )
