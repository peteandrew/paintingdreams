# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0018_auto_20160908_2231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='state',
            field=models.CharField(choices=[('notpaid', 'Not paid'), ('paid', 'Paid'), ('shipped', 'Order shipped')], default='notpaid', max_length=18),
        ),
    ]
