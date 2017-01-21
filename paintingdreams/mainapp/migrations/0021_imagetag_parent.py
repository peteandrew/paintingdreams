# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0020_producttype_subproduct_hide'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagetag',
            name='parent',
            field=models.ForeignKey(blank=True, to='mainapp.ImageTag', default=None, null=True),
        ),
    ]
