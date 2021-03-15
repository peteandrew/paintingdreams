import json
import os
import uuid

from django.db import models
from django.utils.html import format_html

from mainapp.ImageResizer import ImageResizer

def get_webimage_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('images', 'original', filename)


class Webimage(models.Model):
    webimage = models.ImageField(upload_to=get_webimage_path)
    name = models.CharField(max_length=100, blank=True)
    sizes = models.CharField(max_length=255, blank=True)
    order = models.PositiveSmallIntegerField(default=0, blank=True)
    custom_img_sizes = None

    def __str__(self):
        return self.filename()

    def filename(self):
        path = self.webimage.name
        fname = path[path.rfind('/')+1:]
        return fname

    def save(self, *args, **kwargs):
        super(Webimage, self).save(*args, **kwargs)
        sizes = ImageResizer(self.filename()).resize(img_sizes=self.custom_img_sizes)
        self.sizes = json.dumps(sizes)
        super(Webimage, self).save(*args, **kwargs)

    def original_image(self):
        url = '/original_image/' + self.filename()
        return format_html('<a href="' + url + '">Original image</a>')

    class Meta:
        abstract= True
        ordering = ['order']


class FestivalPageWebimage(Webimage):
    festival_page = models.ForeignKey('FestivalPage', related_name='webimages', on_delete=models.CASCADE)
    custom_img_sizes = ['enlargement-no-watermark', 'extra-large-no-watermark']


class ImageWebimage(Webimage):
    image = models.ForeignKey('Image', related_name='webimages', on_delete=models.CASCADE)


class ProductWebimage(Webimage):
    product = models.ForeignKey('Product', related_name='webimages', on_delete=models.CASCADE)


class HomePageWebimage(Webimage):
    link = models.CharField(max_length=100, blank=True)
    enabled = models.BooleanField(default=True)


class FeedbackWebimage(Webimage):
    feedback = models.ForeignKey('Feedback', related_name='webimages', on_delete=models.CASCADE)
    custom_img_sizes = ['standard-no-watermark', 'enlargement-no-watermark']