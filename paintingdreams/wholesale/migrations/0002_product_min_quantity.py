# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wholesale', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='min_quantity',
            field=models.SmallIntegerField(default=0),
        ),
    ]
