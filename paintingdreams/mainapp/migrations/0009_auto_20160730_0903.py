# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_auto_20160730_0825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customer_shipping_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='unique_id',
            field=models.CharField(default='8a23970b-90b7-483f-b9e6-da96565d2997', blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='ordertransaction',
            name='unique_id',
            field=models.CharField(default='953a1038-58e1-47f9-8c98-230d9ea70d5d', blank=True, max_length=50),
        ),
    ]
