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
    temporarily_unavailable = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Special(models.Model):
    name = models.CharField(max_length=30, unique=True)
    postage_option = models.CharField(max_length=8, choices=(('std','std'),('none','none'),('wghtcalc','wghtcalc')))
    display_vat_message = models.BooleanField(default=True)
    display_brexit_message = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class SpecialProductRemoved(models.Model):
    special = models.ForeignKey(Special, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Order(models.Model):
    shop_name = models.CharField(max_length=200)
    shop_address = models.TextField()
    contact_name = models.CharField(max_length=200)
    contact_email = models.EmailField()
    contact_tel = models.CharField(max_length=100)
    special_name = models.CharField(max_length=30)
    postage_option = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)


class OrderLine(models.Model):
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    item_price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.SmallIntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    @property
    def line_price(self):
        return self.item_price * self.quantity
