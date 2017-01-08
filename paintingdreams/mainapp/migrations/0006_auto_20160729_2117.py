# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_auto_20160723_2159'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='customer_address',
        ),
        migrations.AddField(
            model_name='order',
            name='customer_billing_address',
            field=models.ForeignKey(default=1, to='mainapp.UserAddress', related_name='billing_address'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='customer_shipping_address',
            field=models.ForeignKey(default=1, to='mainapp.UserAddress', related_name='shipping_address'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='unique_id',
            field=models.CharField(default='65091c14-3ea5-4f70-9b46-eac06b2fba83', max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='ordertransaction',
            name='unique_id',
            field=models.CharField(default='11f8bc5e-a17f-4420-ba82-67dc33ad0eab', max_length=50, blank=True),
        ),
    ]
