# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0027_auto_20170121_1812'),
    ]

    operations = [
        migrations.AddField(
            model_name='producttype',
            name='index_inline',
            field=models.BooleanField(default=False),
        ),
    ]
