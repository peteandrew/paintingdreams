# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-16 21:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0043_auto_20170812_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='producttype',
            name='product_listing_message',
            field=models.TextField(blank=True),
        ),
    ]
