# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=255)),
                ('price', models.DecimalField(max_digits=6, default=0, decimal_places=2)),
                ('new', models.BooleanField(default=False)),
                ('sold_out', models.BooleanField(default=False)),
                ('category', models.ForeignKey(to='wholesale.Category', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='Special',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('postage_option', models.CharField(max_length=8, choices=[('std', 'std'), ('none', 'none'), ('wghtcalc', 'wghtcalc')])),
            ],
        ),
        migrations.CreateModel(
            name='SpecialProductRemoved',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(to='wholesale.Product', on_delete=models.CASCADE)),
                ('special', models.ForeignKey(to='wholesale.Special', on_delete=models.CASCADE)),
            ],
        ),
    ]
