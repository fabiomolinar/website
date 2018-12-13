from django.db import migrations

def insert_mysite(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    Site.objects.all().delete()

    # Register SITE_ID = 1
    Site.objects.create(id=1, domain='fabiomolinar.com', name='Fabio Molinar')

class Migration(migrations.Migration):

    dependencies = [
        ('sites','0002_alter_domain_unique')
    ]

    operations = [
        migrations.RunPython(insert_mysite)
    ]
