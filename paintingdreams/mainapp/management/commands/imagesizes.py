from django.core.management.base import BaseCommand, CommandError
from mainapp.models import Image

class Command(BaseCommand):
    help = 'Finds webimage dimensions for all Images'

    def handle(self, *args, **options):
        images = Image.objects.all()
        for image in images:
            print(image.slug + "\t" + image.title)
            webimages = image.webimages.all()
            for webimage in webimages:
                print("\t" + str(webimage.webimage) + "\t" + str(webimage.webimage.width) + ' x ' + str(webimage.webimage.height))
            print("\n")
