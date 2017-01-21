# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0022_auto_20170120_1926'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='image_tags',
            new_name='tags',
        ),
    ]
