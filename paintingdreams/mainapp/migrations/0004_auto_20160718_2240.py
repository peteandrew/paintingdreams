# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_auto_20160110_2105'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('unique_id', models.CharField(max_length=50, default='de0685e5-0677-420f-a9ec-bfdf6961f988', blank=True)),
                ('payment_processor', models.CharField(max_length=8, null=True, blank=True, choices=[('paypal', 'PayPal'), ('cardsave', 'CardSave')])),
                ('state', models.CharField(max_length=18, default='started', choices=[('started', 'Started'), ('cancelled', 'Cancelled'), ('complete', 'Complete'), ('failed', 'Failed')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='order',
            name='payment_processor',
        ),
        migrations.AlterField(
            model_name='order',
            name='state',
            field=models.CharField(max_length=18, default='notpaid', choices=[('notpaid', 'Not paid'), ('payed', 'Payed'), ('shipped', 'Order shipped')]),
        ),
        migrations.AlterField(
            model_name='order',
            name='unique_id',
            field=models.CharField(max_length=50, default='49a10654-2997-4e58-b849-547c5a76616a', blank=True),
        ),
        migrations.AddField(
            model_name='ordertransaction',
            name='order',
            field=models.ForeignKey(to='mainapp.Order'),
        ),
    ]
