# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0014_auto_20160821_1445'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderAddress',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('address1', models.CharField(max_length=255)),
                ('address2', models.CharField(max_length=255, blank=True)),
                ('address3', models.CharField(max_length=255, blank=True)),
                ('address4', models.CharField(max_length=255, blank=True)),
                ('city', models.CharField(max_length=255, blank=True)),
                ('state', models.CharField(max_length=255, blank=True)),
                ('post_code', models.CharField(max_length=255, blank=True)),
                ('country', django_countries.fields.CountryField(max_length=2)),
            ],
        ),
        migrations.RemoveField(
            model_name='useraddress',
            name='user',
        ),
        migrations.AlterField(
            model_name='order',
            name='customer_billing_address',
            field=models.ForeignKey(related_name='billing_address', to='mainapp.OrderAddress'),
        ),
        migrations.AlterField(
            model_name='order',
            name='customer_shipping_address',
            field=models.ForeignKey(related_name='shipping_address', blank=True, null=True, to='mainapp.OrderAddress'),
        ),
        migrations.DeleteModel(
            name='UserAddress',
        ),
    ]
