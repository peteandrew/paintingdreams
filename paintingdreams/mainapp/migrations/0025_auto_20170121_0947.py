# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0024_auto_20170120_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageimagetag',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]
