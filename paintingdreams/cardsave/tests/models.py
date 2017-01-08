from django.db import models


class Order(models.Model):
    unique_id = models.CharField(max_length=50)
    total_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
