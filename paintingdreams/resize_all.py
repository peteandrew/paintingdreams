import mainapp.models
import mainapp.ImageResizer

for image in mainapp.models.Image.objects.all():
    print(image)
#    for webimage in image.webimages.all():
#        print(filename)
#        filename = webimage.filename()
#        img = mainapp.ImageResizer.ImageResizer(filename)
#        img.resize()
