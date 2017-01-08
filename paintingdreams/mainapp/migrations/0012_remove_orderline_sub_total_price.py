# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0011_auto_20160730_1605'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderline',
            name='sub_total_price',
        ),
    ]
