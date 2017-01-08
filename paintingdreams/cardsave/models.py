from django.db import models


class PaymentResult(models.Model):
    status_code = models.IntegerField()
    message = models.CharField(max_length=512, blank=True)
    previous_status_code = models.IntegerField(blank=True, null=True)
    previous_message = models.CharField(max_length=512, blank=True)
    cross_reference = models.CharField(max_length=24, blank=True)
    order_id = models.CharField(max_length=50)

    TRANSACTION_TYPE_CHOICES = (
        ('SALE', 'sale'),
        ('PREAUTH', 'preauth')
    )
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPE_CHOICES)

    transaction_datetime = models.DateTimeField() 
