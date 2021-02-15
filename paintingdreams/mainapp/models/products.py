from django.core.exceptions import ValidationError
from django.db import models


SHIPPING_DESTINATION_CHOICES = (
    ('GB', 'United Kingdom'),
    ('EUROPE', 'Europe'),
    ('WORLD', 'Worldwide'),
    ('US', 'United States'),
)


class PostagePrice(models.Model):
    destination = models.CharField(choices=SHIPPING_DESTINATION_CHOICES, max_length=6)
    min_weight = models.PositiveSmallIntegerField(default=0)
    max_weight = models.PositiveSmallIntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    class Meta:
        ordering = ['destination', 'min_weight']

    def __str__(self):
        return self.destination + ' (' + str(self.min_weight) + ' - ' + str(self.max_weight) + ')'


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
    product_listing_message = models.TextField(blank=True)
    stand_alone = models.BooleanField(default=False)
    inherit_stand_alone = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    special_offer_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
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
    def special_offer(self):
        if self.inherit_price and self.parent:
            return self.parent.special_offer
        elif self.special_offer_price:
            return True
        return False

    @property
    def price_final(self):
        if self.inherit_price and self.parent:
            return self.parent.price_final
        elif self.special_offer_price:
            return self.special_offer_price
        return self.price

    @property
    def old_price_final(self):
        if self.inherit_price and self.parent:
            return self.parent.old_price_final
        return self.price

    def shipping_weight_final(self, destination=None):
        # Return inherited from type here
        if self.inherit_shipping_weight and self.parent:
            return self.parent.shipping_weight_final(destination)
        else:
            # If ProductTypeDestinationShippingWeightOverride exists for destination,
            # use that shipping_weight
            # else use this ProductType shipping_weight
            try:
                shipping_weight_override = self.destination_shipping_weight_overrides.get(
                    destination=destination,
                )
                return shipping_weight_override.shipping_weight
            except ProductTypeDestinationShippingWeightOverride.DoesNotExist:
                return self.shipping_weight

    def shipping_weight_multiple_final(self, destination=None):
        if self.inherit_shipping_weight_multiple and self.parent:
            return self.parent.shipping_weight_multiple_final(destination)
        else:
            # If ProductTypeDestinationShippingWeightOverride exists for destination,
            # and it has shipping_weight_multiple set use that otherwise use shipping_weight
            # else use this ProductType shipping_weight_multiple if it exists
            # else fallback to shipping_weight_final
            try:
                shipping_weight_override = self.destination_shipping_weight_overrides.get(
                    destination=destination,
                )
                if shipping_weight_override.shipping_weight_multiple > 0:
                    return shipping_weight_override.shipping_weight_multiple
                else:
                    return shipping_weight_override.shipping_weight
            except ProductTypeDestinationShippingWeightOverride.DoesNotExist:
                if self.shipping_weight_multiple > 0:
                    return self.shipping_weight_multiple
                else:
                    return self.shipping_weight_final(destination)


class ProductTypeDestinationShippingWeightOverride(models.Model):
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.CASCADE,
        related_name='destination_shipping_weight_overrides',
    )
    destination = models.CharField(choices=SHIPPING_DESTINATION_CHOICES, max_length=6)
    shipping_weight = models.IntegerField(default=0)
    shipping_weight_multiple = models.IntegerField(default=0)

    class Meta:
        unique_together = ['product_type', 'destination']
        verbose_name = 'destination shipping weight override'


class ProductManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('product_type').select_related('image')


class Product(models.Model):
    code = models.CharField(max_length=20, blank=True)
    image = models.ForeignKey('Image', null=True, default=None, blank=True, on_delete=models.CASCADE)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    hidden = models.BooleanField(default=False)
    sold_out = models.BooleanField(default=False)
    more_due = models.BooleanField(default=True)
    due_text = models.CharField(max_length=255, blank=True)
    extra_description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('ProductTag', default=None, blank=True)
    product_type_order = models.IntegerField(default=0)
    temporarily_unavailable = models.BooleanField(default=False)
    stock_count = models.PositiveIntegerField(default=0)
    special_offer_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    objects = ProductManager()

    class Meta:
        unique_together = ("image", "product_type")
        ordering = ['image__title', 'product_type__title']
        permissions = (
            ("change_product_stock_count", "Can change product stock count"),
        )


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

    @property
    def special_offer(self):
        if self.special_offer_price or self.product_type.special_offer:
            return True
        return False

    @property
    def price(self):
        if self.special_offer_price:
            return self.special_offer_price
        return self.product_type.price_final

    @property
    def old_price(self):
        if self.special_offer_price:
            return self.product_type.price_final
        return self.product_type.old_price_final


class ProductAdditionalProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    additional_product = models.ForeignKey(Product, related_name="additional_product", on_delete=models.CASCADE)


class ProductTypeAdditionalProduct(models.Model):
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


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


class HomePageProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']