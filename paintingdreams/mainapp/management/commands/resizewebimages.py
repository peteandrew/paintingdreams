import json
from django.core.management.base import BaseCommand, CommandError
from mainapp.ImageResizer import ImageResizer
from mainapp.models import (
    ImageWebimage,
    ProductWebimage,
    FestivalPageWebimage,
    HomePageWebimage,
    FeedbackWebimage,
)

class Command(BaseCommand):
    help = 'Resize webimages'

    @staticmethod
    def resize_webimages(webimages_qs):
        for webimage in webimages_qs:
            print(str(webimage))
            sizes = ImageResizer(webimage.filename()).resize(img_sizes=webimage.custom_img_sizes)
            webimage.sizes = json.dumps(sizes)
            webimage.save()
            print("\n")

    def add_arguments(self, parser):
        parser.add_argument(
            '--type',
            choices=['images', 'products', 'festival', 'home', 'feedback', 'all'],
            required=True
        )

    def handle(self, *args, **options):
        if options['type'] in ['images', 'all']:
            print("** Resizing image webimages **\n")
            Command.resize_webimages(ImageWebimage.objects.all())

        if options['type'] in ['products', 'all']:
            print("** Resizing product webimages **\n")
            Command.resize_webimages(ProductWebimage.objects.all())

        if options['type'] in ['festival', 'all']:
            print("** Resizing festival webimages **\n")
            Command.resize_webimages(FestivalPageWebimage.objects.all())

        if options['type'] in ['home', 'all']:
            print("** Resizing home webimages **\n")
            Command.resize_webimages(HomePageWebimage.objects.all())

        if options['type'] in ['feedback', 'all']:
            print("** Resizing feedback webimages **\n")
            Command.resize_webimages(FeedbackWebimage.objects.all())
