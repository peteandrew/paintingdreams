# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0017_auto_20160828_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='unique_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='ordertransaction',
            name='order',
            field=models.ForeignKey(to='mainapp.Order', to_field='unique_id'),
        ),
        migrations.AlterField(
            model_name='ordertransaction',
            name='unique_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
