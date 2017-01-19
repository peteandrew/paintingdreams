# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0019_auto_20170102_0007'),
    ]

    operations = [
        migrations.AddField(
            model_name='producttype',
            name='subproduct_hide',
            field=models.BooleanField(default=False),
        ),
    ]
