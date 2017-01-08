# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0012_remove_orderline_sub_total_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderline',
            old_name='price',
            new_name='item_price',
        ),
        migrations.RemoveField(
            model_name='order',
            name='sub_total_price',
        ),
        migrations.RemoveField(
            model_name='order',
            name='total_price',
        ),
        migrations.AddField(
            model_name='orderline',
            name='item_weight',
            field=models.IntegerField(default=0),
        ),
    ]
