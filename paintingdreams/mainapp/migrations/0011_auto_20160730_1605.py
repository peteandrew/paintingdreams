# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0010_auto_20160730_1556'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='unique_id',
            field=models.UUIDField(editable=False, default=uuid.uuid4),
        ),
        migrations.AddField(
            model_name='ordertransaction',
            name='unique_id',
            field=models.UUIDField(editable=False, default=uuid.uuid4),
        ),
    ]
