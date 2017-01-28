from django.core.management.base import BaseCommand, CommandError
from mainapp.models import Image, Product, ImageResizer

class Command(BaseCommand):
    help = 'Resize webimages'


    @staticmethod
    def resize_item_webimage(item):
        webimages = item.webimages.all()
        for webimage in webimages:
            print("\t" + str(webimage))
            sizes = ImageResizer(webimage.filename()).resize()
            webimage.sizes = sizes
            webimage.save()



    def handle(self, *args, **options):
        print("** Resizing image webimages **\n")
        images = Image.objects.all()
        for image in images:
            print(image.slug + "\t" + image.title)
            Command.resize_item_webimage(image)
            print("\n")

        print("** Resizing product webimages **\n")
        products = Product.objects.all()
        for product in products:
            print(str(product.image) + "\t" + str(product.product_type))
            Command.resize_item_webimage(product)
            print("\n")
