import pytz
from datetime import datetime
from django.db import models


class DiscountCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    disabled = models.BooleanField(default=False)
    valid_from = models.DateTimeField(blank=True, null=True)
    valid_until = models.DateTimeField(blank=True, null=True)

    def is_valid(self):
        if self.disabled:
            return False
        now = datetime.now(pytz.utc)
        if (self.valid_from and self.valid_from > now) or (self.valid_until and self.valid_until < now):
            return False
        return True

    def __str__(self):
        return self.code


class DiscountCodeProduct(models.Model):
    discount_code = models.ForeignKey(
        DiscountCode,
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
    )
    discounted_price = models.DecimalField(
        blank=True,
        max_digits=6,
        decimal_places=2,
        default=0,
    )

    class Meta:
        unique_together = ('discount_code', 'product')