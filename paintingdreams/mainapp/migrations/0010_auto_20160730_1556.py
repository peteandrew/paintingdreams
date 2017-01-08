# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_auto_20160730_0903'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='unique_id',
        ),
        migrations.RemoveField(
            model_name='ordertransaction',
            name='unique_id',
        ),
    ]
