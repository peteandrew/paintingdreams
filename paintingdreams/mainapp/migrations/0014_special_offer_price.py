# Generated by Django 2.2.17 on 2020-12-30 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0013_auto_20201025_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='special_offer_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6),
        ),
    ]