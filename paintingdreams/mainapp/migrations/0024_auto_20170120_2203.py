# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0023_auto_20170120_2013'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='imagetag',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='imagetag',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]
