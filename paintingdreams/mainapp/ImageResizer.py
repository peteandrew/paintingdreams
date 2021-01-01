from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
import os
import math

# import logging
# logger = logging.getLogger('django')

class ImageResizer:

    def __init__(self, image_filename):
        self.image_filename = image_filename


    @staticmethod
    def build_full_path(img_type_dir, img_filename):
        return os.path.join(settings.MEDIA_ROOT, 'images', img_type_dir, img_filename)


    @staticmethod
    def calc_new_size(original_size, new_longest_side):
        if original_size[0] > original_size[1]:
            width_longest = True
            cur_longest_side = original_size[0]
        else:
            width_longest = False
            cur_longest_side = original_size[1]

        # If the current longest side is less than or equal to the new longest side
        # then we don't need to do any resizing, return current size
        if cur_longest_side <= new_longest_side:
            return original_size

        ratio = original_size[1] / original_size[0]

        if width_longest:
            new_size = (new_longest_side, round(new_longest_side * ratio))
        else:
            new_size = (round(new_longest_side / ratio), new_longest_side)

        return new_size


    @staticmethod
    def add_watermark(image, longest_side_max_length, fontsize_base):
        longest_side_length = image.size[0]
        if image.size[1] > image.size[0]:
            longest_side_length = image.size[1]

        fontsize_scale = (longest_side_length / longest_side_max_length)
        print('calculated scale:' + str(fontsize_scale))
        if fontsize_scale < 1:
            fontsize_scale = fontsize_scale * 0.95
        print('adjusted scale:' + str(fontsize_scale))
        fontsize = int(fontsize_base * fontsize_scale)
        print('fontsize base:' + str(fontsize_base))
        print('adjusted fontsize:' + str(fontsize))

        fnt = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', fontsize)
        tmpdraw = ImageDraw.Draw(image)
        textsize = tmpdraw.textsize('www.paintingdreams.co.uk', font=fnt)

        watermark_layer = Image.new("RGBA", textsize, (255,255,255,0))
        watermark_draw = ImageDraw.Draw(watermark_layer, "RGBA")
        watermark_draw.text((0,0), "www.paintingdreams.co.uk", font=fnt, fill=(230,230,230,70))

        angle = math.degrees( math.atan2(image.size[1], image.size[0]) )
        watermark_layer = watermark_layer.rotate(angle, expand=True)

        left = int((image.size[0] - watermark_layer.size[0]) / 2)
        top = int((image.size[1] - watermark_layer.size[1]) / 2)

        image.paste(watermark_layer, (left,top), watermark_layer)


    def resize(self, img_sizes=None):
        if not img_sizes:
            img_sizes = ['standard', 'enlargement', 'thumbnail']

        sizes = {}

        for img_size in img_sizes:
            try:
                img_size_settings = settings.IMAGE_SIZES[img_size]
            except KeyError:
                continue

            img_full_path = ImageResizer.build_full_path('original', self.image_filename)
            self.img_original = Image.open(img_full_path)

            longest_side_max_length = img_size_settings['longest_side']
            new_size = ImageResizer.calc_new_size(self.img_original.size, longest_side_max_length)
            new_img = self.img_original.resize(new_size, Image.BICUBIC)

            if img_size_settings['watermark']:
                fontsize_base = img_size_settings['watermark_base_size']
                ImageResizer.add_watermark(new_img, longest_side_max_length, fontsize_base)

            img_full_path = ImageResizer.build_full_path(img_size_settings['path'], self.image_filename)
            new_img.save(img_full_path, 'jpeg', quality=85)

            sizes[img_size] = new_size

        return sizes
