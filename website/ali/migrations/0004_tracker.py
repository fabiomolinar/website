# Generated by Django 2.1.4 on 2018-12-31 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ali', '0003_auto_20181219_1052'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tracker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_text', models.TextField(verbose_name='text used on the search query')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
            ],
        ),
    ]
