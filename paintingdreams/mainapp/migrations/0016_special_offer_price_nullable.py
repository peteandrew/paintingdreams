# Generated by Django 2.2.17 on 2020-12-31 15:39

from django.db import migrations, models


def set_special_offers_null(apps, schmea_editor):
    ProductType = apps.get_model('mainapp', 'ProductType')
    for product_type in ProductType.objects.filter(special_offer_price=0):
        product_type.special_offer_price = None
        product_type.save()
    Product = apps.get_model('mainapp', 'Product')
    for product in Product.objects.filter(special_offer_price=0):
        product.special_offer_price = None
        product.save()

def unset_special_offers_null(apps, schmea_editor):
    ProductType = apps.get_model('mainapp', 'ProductType')
    for product_type in ProductType.objects.filter(special_offer_price__isnull=True):
        product_type.special_offer_price = 0
        product_type.save()
    Product = apps.get_model('mainapp', 'Product')
    for product in Product.objects.filter(special_offer_price__isnull=True):
        product.special_offer_price = 0
        product.save()


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0015_product_type_special_offer_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='special_offer_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='producttype',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='producttype',
            name='special_offer_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
        migrations.RunPython(set_special_offers_null, unset_special_offers_null)
    ]
