# Generated by Django 2.2.17 on 2021-04-04 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0021_allow_hide_creation_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='customer_phone',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
