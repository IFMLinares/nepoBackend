from django.db import migrations

def create_default_uoms(apps, schema_editor):
    UnitOfMeasure = apps.get_model('inventory', 'UnitOfMeasure')
    uoms = [
        {'name': 'Unidad', 'abbreviation': 'Und'},
        {'name': 'Kilogramos', 'abbreviation': 'Kg'},
        {'name': 'Metros', 'abbreviation': 'm'},
    ]
    for uom in uoms:
        UnitOfMeasure.objects.get_or_create(
            abbreviation=uom['abbreviation'], 
            defaults={'name': uom['name']}
        )

class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_uoms),
    ]
