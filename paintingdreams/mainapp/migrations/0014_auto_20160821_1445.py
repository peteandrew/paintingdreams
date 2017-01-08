# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0013_auto_20160821_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderline',
            name='item_price',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name='orderline',
            name='item_weight',
            field=models.IntegerField(),
        ),
    ]
