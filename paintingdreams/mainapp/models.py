from functools import reduce
import operator
import uuid
import os
import json

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django_countries.fields import CountryField

from django.utils.html import format_html

from mainapp.ImageResizer import ImageResizer

import logging
logger = logging.getLogger('django')


def get_webimage_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('images', 'original', filename)


class ImageTag(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name',]

    def __str__(self):
        return self.name


class Image(models.Model):
    ORIGINAL_CHOICES = (
        ('notavailable', 'Not available'),
        ('available', 'Available'),
        ('sold', 'Sold'),
    )

    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    original = models.CharField(choices=ORIGINAL_CHOICES, max_length=15, default='notavailable')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    products = models.ManyToManyField('ProductType', through='Product')
    galleries = models.ManyToManyField('Gallery', through='ImageGallery')
    tags = models.ManyToManyField('ImageTag', default=None, blank=True)

    class Meta:
        ordering = ['title',]

    def __str__(self):
        return self.title


class Webimage(models.Model):
    webimage = models.ImageField(upload_to=get_webimage_path)
    name = models.CharField(max_length=100, blank=True)
    sizes = models.CharField(max_length=255, blank=True)
    order = models.PositiveSmallIntegerField(default=0, blank=True)

    def __str__(self):
        return self.filename()

    def filename(self):
        path = self.webimage.name
        fname = path[path.rfind('/')+1:]
        return fname

    def save(self, *args, **kwargs):
        super(Webimage, self).save(*args, **kwargs)
        sizes = ImageResizer(self.filename()).resize()
        self.sizes = json.dumps(sizes)
        super(Webimage, self).save(*args, **kwargs)

    def original_image(self):
        url = '/original_image/' + self.filename()
        return format_html('<a href="' + url + '">Original image</a>')

    class Meta:
        abstract= True
        ordering = ['order']


class ImageWebimage(Webimage):
    image = models.ForeignKey('Image', related_name='webimages', on_delete=models.CASCADE)


class ProductWebimage(Webimage):
    product = models.ForeignKey('Product', related_name='webimages', on_delete=models.CASCADE)


class HomePageWebimage(Webimage):
    link = models.CharField(max_length=50, blank=True)
    enabled = models.BooleanField(default=True)


class ProductType(models.Model):
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self', null=True, default=None, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    displayname = models.CharField(max_length=100, blank=True)
    inherit_displayname = models.BooleanField(default=False)
    subproduct_hide = models.BooleanField(default=False)
    index_inline = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    inherit_description = models.BooleanField(default=False)
    stand_alone = models.BooleanField(default=False)
    inherit_stand_alone = models.BooleanField(default=True)
    price = models.DecimalField(blank=True, max_digits=6, decimal_places=2, default=0)
    inherit_price = models.BooleanField(default=True)
    shipping_weight = models.IntegerField(default=0)
    inherit_shipping_weight = models.BooleanField(default=False)
    shipping_weight_multiple = models.IntegerField(default=0)
    inherit_shipping_weight_multiple = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['title',]

    def __str__(self):
        return self.title

    def children(self, prod_types=None, parent=None, level=1):
        if not prod_types:
            prod_types = list(ProductType.objects.all().order_by('parent_id', 'order'))
            if len(prod_types) == 0:
                return []
        if not parent:
            parent = self

        children = []
        for prod_type in prod_types:
            if prod_type.parent_id == parent.id:
                prod_type_children = self.children(prod_types, prod_type, level + 1)
                branch_ids = [prod_type.id]
                for child in prod_type_children:
                    branch_ids += child['branch_ids']
                children += [{'product_type': prod_type, 'children': prod_type_children, 'branch_ids': branch_ids}]

        return children

    def parents(self):
        if not self.parent:
            return []
        parents = [self.parent]
        parents += self.parent.parents()
        return parents

    @property
    def displayname_final(self):
        if self.inherit_displayname and self.parent:
            return self.parent.displayname_final
        else:
            if not self.displayname.strip():
                return self.title
            else:
                return self.displayname

    @property
    def description_final(self):
        if self.inherit_description and self.parent:
            return self.parent.description_final
        else:
            return self.description

    @property
    def stand_alone_final(self):
        if self.inherit_stand_alone and self.parent:
            return self.parent.stand_alone_final
        else:
            return self.stand_alone

    @property
    def price_final(self):
        if self.inherit_price and self.parent:
            return self.parent.price_final
        else:
            return self.price

    @property
    def shipping_weight_final(self):
        if self.inherit_shipping_weight and self.parent:
            return self.parent.shipping_weight_final
        else:
            return self.shipping_weight

    @property
    def shipping_weight_multiple_final(self):
        if self.inherit_shipping_weight_multiple and self.parent:
            return self.parent.shipping_weight_multiple_final
        elif self.shipping_weight_multiple > 0:
            return self.shipping_weight_multiple
        else:
            return self.shipping_weight_final


class Gallery(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', null=True, default=None, blank=True, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order',]

    def __str__(self):
        return self.name

    def children(self, galleries=None, parent=None, level=1):
        if not galleries:
            galleries = list(Gallery.objects.all().order_by('parent_id', 'order'))
            if len(galleries) == 0:
                return []
        if not parent:
            parent = self

        children = []
        for gallery in galleries:
            if gallery.parent_id == parent.id:
                gallery_children = self.children(galleries, gallery, level + 1)
                branch_ids = [gallery.id]
                for child in gallery_children:
                    branch_ids += child['branch_ids']
                children += [{'gallery': gallery, 'children': gallery_children, 'branch_ids': branch_ids}]

        return children


class ImageGallery(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['gallery', 'order',]


class ProductTag(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name',]

    def __str__(self):
        return self.name


class Product(models.Model):
    code = models.CharField(max_length=20, blank=True)
    image = models.ForeignKey(Image, null=True, default=None, blank=True, on_delete=models.CASCADE)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    sold_out = models.BooleanField(default=False)
    more_due = models.BooleanField(default=True)
    due_text = models.CharField(max_length=255, blank=True)
    extra_description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('ProductTag', default=None, blank=True)
    product_type_order = models.IntegerField(default=0)

    class Meta:
        unique_together = ("image", "product_type")
        ordering = ['product_type_order']

    def clean(self):
        if not self.image and not self.product_type.stand_alone:
            raise ValidationError({'product_type': 'If no image specified, product_type must be stand alone.'})

    def __str__(self):
        string = ""
        if self.image:
            string += str(self.image) + " - "
        string += str(self.product_type)
        return string

    @property
    def displayname(self):
        string = ""
        if self.image:
            string += str(self.image) + " - "
        string += self.product_type.displayname_final
        return string


# class UserAddress(models.Model):
#     user = models.ForeignKey(User, blank=True, null=True)
#     address1 = models.CharField(max_length=255)
#     address2 = models.CharField(max_length=255, blank=True)
#     address3 = models.CharField(max_length=255, blank=True)
#     address4 = models.CharField(max_length=255, blank=True)
#     city = models.CharField(max_length=255, blank=True)
#     state = models.CharField(max_length=255, blank=True)
#     post_code = models.CharField(max_length=255, blank=True)
#     country = CountryField()


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
            ret += ', ' + attr
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
    product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.CASCADE)
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


class PostagePrice(models.Model):
    DESTINATION_CHOICES = (
        ('GB', 'United Kingdom'),
        ('EUROPE', 'Europe'),
        ('WORLD', 'Worldwide')
    )

    destination = models.CharField(choices=DESTINATION_CHOICES, max_length=6)
    min_weight = models.PositiveSmallIntegerField(default=0)
    max_weight = models.PositiveSmallIntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    class Meta:
        ordering = ['destination', 'min_weight']

    def __str__(self):
        return self.destination + ' (' + str(self.min_weight) + ' - ' + str(self.max_weight) + ')'
