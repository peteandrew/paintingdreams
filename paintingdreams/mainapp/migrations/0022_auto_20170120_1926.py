# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0021_imagetag_parent'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageImageTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('order', models.IntegerField()),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.RemoveField(
            model_name='image',
            name='tags',
        ),
        migrations.AddField(
            model_name='imageimagetag',
            name='image',
            field=models.ForeignKey(to='mainapp.Image'),
        ),
        migrations.AddField(
            model_name='imageimagetag',
            name='image_tag',
            field=models.ForeignKey(to='mainapp.ImageTag'),
        ),
        migrations.AddField(
            model_name='image',
            name='image_tags',
            field=models.ManyToManyField(through='mainapp.ImageImageTag', to='mainapp.ImageTag'),
        ),
    ]
