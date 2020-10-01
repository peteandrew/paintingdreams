from django.db import models


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