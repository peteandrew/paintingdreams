from django.db import models


class FestivalPage(models.Model):
    slug = models.CharField(max_length=30)
    title = models.CharField(max_length=255)
    short_title = models.CharField(max_length=50, blank=True)
    dates = models.CharField(max_length=255, blank=True)
    details = models.TextField(blank=True)
    products = models.ManyToManyField('Product', through='FestivalPageProduct')

    def __str__(self):
        return self.title


class FestivalPageProduct(models.Model):
    festival_page = models.ForeignKey('FestivalPage', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['festival_page', 'order',]