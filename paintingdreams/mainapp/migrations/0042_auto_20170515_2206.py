# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-15 22:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0041_auto_20170329_2208'),
    ]

    operations = [
        migrations.CreateModel(
            name='HolidayMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('website_message', models.TextField(blank=True)),
                ('email_message', models.TextField(blank=True)),
                ('wholesale_message', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['-start', '-end'],
            },
        ),
        migrations.AlterIndexTogether(
            name='holidaymessage',
            index_together=set([('start', 'end')]),
        ),
    ]
