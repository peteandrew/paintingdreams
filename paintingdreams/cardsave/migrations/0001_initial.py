# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentResult',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('status_code', models.IntegerField()),
                ('message', models.CharField(max_length=512, blank=True)),
                ('previous_status_code', models.IntegerField(null=True, blank=True)),
                ('previous_message', models.CharField(max_length=512, blank=True)),
                ('cross_reference', models.CharField(max_length=24, blank=True)),
                ('order_id', models.CharField(max_length=50)),
                ('transaction_type', models.CharField(max_length=7, choices=[('SALE', 'sale'), ('PREAUTH', 'preauth')])),
                ('transaction_datetime', models.DateTimeField()),
            ],
        ),
    ]
