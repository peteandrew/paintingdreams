import uuid

from django.db import models
from django_countries.fields import CountryField


class OrderAddress(models.Model):
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True)
    address3 = models.CharField(max_length=255, blank=True)
    address4 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    post_code = models.CharField(max_length=255, blank=True)
    country = CountryField()

    def __addAttribute(self, ret, attr):
        if attr != '':
            ret += ', ' + str(attr)
        return ret

    def __str__(self):
        ret = self.address1
        ret = self.__addAttribute(ret, self.address2)
        ret = self.__addAttribute(ret, self.address3)
        ret = self.__addAttribute(ret, self.address4)
        ret = self.__addAttribute(ret, self.city)
        ret = self.__addAttribute(ret, self.state)
        ret = self.__addAttribute(ret, self.post_code)
        ret = self.__addAttribute(ret, self.country.name)
        return ret


class Order(models.Model):
    STATE_CHOICES = (
        ('notpaid', 'Not paid'),
        ('paid', 'Paid'),
        ('shipped', 'Order shipped'),
    )

    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    customer_id = models.IntegerField(blank=True, null=True)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    billing_address = models.ForeignKey(OrderAddress, related_name='order_billing_address', on_delete=models.CASCADE)
    shipping_name = models.CharField(max_length=100, blank=True, null=True)
    shipping_address = models.ForeignKey(OrderAddress, blank=True, null=True, related_name='order_shipping_address', on_delete=models.CASCADE)
    # Store postage price in order record rather than calculating on the fly as postage postage_prices
    # may change and we don't want to affect historic orders
    postage_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    state = models.CharField(choices=STATE_CHOICES, max_length=18, default='notpaid')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = (
            ("view_order", "Can view orders"),
        )

    @property
    def current_transaction(self):
        return self.ordertransaction_set.filter(state='started').order_by('-updated').first()

    @property
    def last_transaction(self):
        return self.ordertransaction_set.order_by('-updated').first()

    @property
    def sub_total_price(self):
        sub_total_price = 0
        for order_line in self.orderline_set.all():
            sub_total_price += order_line.line_price
        return sub_total_price

    @property
    def order_weight(self):
        order_weight = 0
        for order_line in self.orderline_set.all():
            order_weight += order_line.line_weight
        return order_weight

    @property
    def total_price(self):
        return float(self.sub_total_price) + float(self.postage_price)


class OrderLine(models.Model):
    # We store product title, price and weight here instead of just referring
    # to the product object as these values may change and we don't want to
    # affect historic orders
    product = models.ForeignKey('Product', blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    item_price = models.DecimalField(max_digits=6, decimal_places=2)
    item_weight = models.IntegerField()
    quantity = models.SmallIntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    @property
    def line_price(self):
        return self.item_price * self.quantity

    @property
    def line_weight(self):
        return self.item_weight * self.quantity


class OrderTransaction(models.Model):
    PAYMENT_PROCESSOR_CHOICES = (
        ('paypal', 'PayPal'),
        ('cardsave', 'CardSave'),
    )

    STATE_CHOICES = (
        ('started', 'Started'),
        ('cancelled', 'Cancelled'),
        ('complete', 'Complete'),
        ('failed', 'Failed'),
    )

    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    order = models.ForeignKey(Order, to_field='unique_id', on_delete=models.CASCADE)
    payment_processor = models.CharField(choices=PAYMENT_PROCESSOR_CHOICES, max_length=8)
    state = models.CharField(choices=STATE_CHOICES, max_length=18, default='started')
    message = models.CharField(max_length=512, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        return self.order.total_price

    @property
    def message_info(self):
        if self.payment_processor == 'cardsave' and self.message == 'Card declined: AVS policy':
            return "This means that the billing address you entered doesn't match the address your card issuer has on file. Please double check your billing address and try again."
        else:
            return ''