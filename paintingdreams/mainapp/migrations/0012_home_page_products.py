# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-10-22 09:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0011_add_orderline_discount'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePageProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Product')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
