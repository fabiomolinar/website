# Generated by Django 2.1.4 on 2018-12-19 07:33

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AliSearch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_text', models.TextField(verbose_name='text used on the search query')),
                ('results', models.IntegerField(verbose_name='total amount of items found by the query')),
                ('walled_brands', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(verbose_name='name of the highlighted brands'), size=None)),
                ('currency', models.CharField(max_length=9)),
                ('max_price', models.FloatField(verbose_name='corrected maximum price')),
                ('min_price', models.FloatField(verbose_name='corrected minimum price')),
                ('average', models.FloatField(verbose_name='corrected average price')),
                ('median', models.FloatField(verbose_name='corrected median price')),
                ('stddev', models.FloatField(verbose_name='corrected standard deviation price')),
                ('number_points', models.IntegerField(verbose_name='number of items used on the corrected calculations')),
                ('max_price_nc', models.FloatField(verbose_name='non-corrected maximum price')),
                ('min_price_nc', models.FloatField(verbose_name='non-corrected minimum price')),
                ('average_nc', models.FloatField(verbose_name='non-corrected average price')),
                ('median_nc', models.FloatField(verbose_name='non-corrected median rice')),
                ('stddev_nc', models.FloatField(verbose_name='non-corrected standard deviation price')),
                ('number_points_nc', models.IntegerField(verbose_name='number of items used on the non-corrected calculations')),
                ('used_url', models.URLField(max_length=1000, verbose_name='URL used to retrieve the data')),
                ('project', models.CharField(max_length=51, verbose_name='name of the Scrapy project')),
                ('spider', models.CharField(max_length=51, verbose_name='name of the Scrapy spider')),
                ('server_name', models.CharField(max_length=51, verbose_name='server name')),
                ('date_created', models.DateTimeField(verbose_name='date the data was collected')),
            ],
        ),
    ]
