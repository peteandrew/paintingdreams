# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-26 20:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wholesale', '0002_product_min_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='temporarily_unavailable',
            field=models.BooleanField(default=False),
        ),
    ]
