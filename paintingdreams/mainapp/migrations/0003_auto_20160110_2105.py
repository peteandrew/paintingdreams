# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_auto_20160106_0010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='unique_id',
            field=models.CharField(max_length=50, blank=True, default='0b175868-e4c3-447f-9242-03ee58cce112'),
        ),
    ]
