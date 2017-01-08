# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_auto_20160729_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customer_shipping_address',
            field=models.ForeignKey(to='mainapp.UserAddress', null=True, related_name='shipping_address', blank=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='unique_id',
            field=models.CharField(max_length=50, default='309ebef0-5f7e-4fa3-800a-41a8b34ab3cb', blank=True),
        ),
        migrations.AlterField(
            model_name='ordertransaction',
            name='unique_id',
            field=models.CharField(max_length=50, default='12dbed64-35fb-4ffe-8edb-37a3c94922bd', blank=True),
        ),
    ]
