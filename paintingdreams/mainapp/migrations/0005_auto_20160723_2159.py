# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_auto_20160718_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='unique_id',
            field=models.CharField(blank=True, default='db0cdfcb-d038-4f62-ade4-9127fea31022', max_length=50),
        ),
        migrations.AlterField(
            model_name='ordertransaction',
            name='payment_processor',
            field=models.CharField(default='paypal', max_length=8, choices=[('paypal', 'PayPal'), ('cardsave', 'CardSave')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ordertransaction',
            name='unique_id',
            field=models.CharField(blank=True, default='8be1b8ff-8475-471c-bf4e-ea6ecb9942bb', max_length=50),
        ),
    ]
