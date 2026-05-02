from django.db import migrations

def create_seeds(apps, schema_editor):
    Currency = apps.get_model('payments', 'Currency')
    PaymentType = apps.get_model('payments', 'PaymentType')
    PaymentMethod = apps.get_model('payments', 'PaymentMethod')

    # Currencies
    usd, _ = Currency.objects.get_or_create(code='USD', defaults={'name': 'Dólares', 'symbol': '$'})
    ves, _ = Currency.objects.get_or_create(code='VES', defaults={'name': 'Bolívares', 'symbol': 'Bs'})

    # Payment Types
    cash, _ = PaymentType.objects.get_or_create(name='Efectivo')
    transfer, _ = PaymentType.objects.get_or_create(name='Transferencia / Pago Móvil')
    card, _ = PaymentType.objects.get_or_create(name='Tarjeta')

    # Mapping existing data
    for method in PaymentMethod.objects.all():
        if not method.currency:
            # Por defecto si el nombre dice Bolivares o Dolares
            if 'bolivares' in method.name.lower():
                method.currency = ves
            elif 'dolares' in method.name.lower():
                method.currency = usd
            else:
                method.currency = usd # Default

        if not method.payment_type:
            # Mapear desde el antiguo field si existe
            old_type = getattr(method, 'method_type', 'CASH')
            if old_type == 'CASH':
                method.payment_type = cash
            elif old_type == 'TRANSFER':
                method.payment_type = transfer
            elif old_type == 'CARD':
                method.payment_type = card
            else:
                method.payment_type = cash
        
        method.save()

class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_currency_paymenttype_alter_paymentmethod_options_and_more'),
    ]

    operations = [
        migrations.RunPython(create_seeds),
    ]
