from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Product(models.Model):
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    new = models.BooleanField(default=False)
    sold_out = models.BooleanField(default=False)
    min_quantity = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.title


class Special(models.Model):
    name = models.CharField(max_length=30, unique=True)
    postage_option = models.CharField(max_length=8, choices=(('std','std'),('none','none'),('wghtcalc','wghtcalc')))


class SpecialProductRemoved(models.Model):
    special = models.ForeignKey(Special, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
