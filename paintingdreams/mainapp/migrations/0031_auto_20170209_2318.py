# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-09 23:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0030_auto_20170205_2137'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='imageimagetag',
            options={'ordering': ['image_tag', 'order']},
        ),
    ]