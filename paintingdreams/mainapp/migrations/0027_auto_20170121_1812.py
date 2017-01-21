# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0026_auto_20170121_1315'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={'ordering': ['title']},
        ),
        migrations.AlterModelOptions(
            name='producttype',
            options={'ordering': ['title']},
        ),
    ]
