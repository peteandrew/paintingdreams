# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0016_auto_20160828_1436'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='customer_shipping_name',
            new_name='shipping_name',
        ),
    ]
