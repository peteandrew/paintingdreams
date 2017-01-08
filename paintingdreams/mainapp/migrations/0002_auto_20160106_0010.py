# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Tag',
            new_name='ImageTag',
        ),
        migrations.AddField(
            model_name='product',
            name='code',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='unique_id',
            field=models.CharField(max_length=50, blank=True, default='0fb0fe42-013b-42bd-829b-5b1ff997105f'),
        ),
    ]
