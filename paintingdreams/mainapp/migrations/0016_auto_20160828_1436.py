# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0015_auto_20160823_2206'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='customer_billing_address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='customer_shipping_address',
        ),
        migrations.AddField(
            model_name='order',
            name='billing_address',
            field=models.ForeignKey(to='mainapp.OrderAddress', default=None, related_name='order_billing_address'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address',
            field=models.ForeignKey(to='mainapp.OrderAddress', null=True, blank=True, related_name='order_shipping_address'),
        ),
    ]
