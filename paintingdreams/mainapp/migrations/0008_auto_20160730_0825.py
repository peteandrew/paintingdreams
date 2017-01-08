# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_auto_20160730_0727'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='customer_shipping_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='order',
            name='unique_id',
            field=models.CharField(blank=True, max_length=50, default='0f65a980-cb84-4d28-a3a9-f27e46a1bdb0'),
        ),
        migrations.AlterField(
            model_name='ordertransaction',
            name='unique_id',
            field=models.CharField(blank=True, max_length=50, default='e522a198-80eb-4ccf-b4a5-49be13b07c70'),
        ),
    ]
