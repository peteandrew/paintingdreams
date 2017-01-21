# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0025_auto_20170121_0947'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['product_type_order']},
        ),
        migrations.AlterModelOptions(
            name='producttype',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='product',
            name='product_type_order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='producttype',
            name='order',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together=set([('image', 'product_type')]),
        ),
    ]
