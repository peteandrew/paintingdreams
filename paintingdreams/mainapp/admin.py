from django.contrib import admin
from mainapp.models import (
    Image,
    ImageTag,
    ImageWebimage,
    ProductType,
    Gallery,
    ImageGallery,
    ProductTag,
    Product,
    ProductWebimage,
    PostagePrice,
    HomePageWebimage,
    HolidayMessage,
    ProductTypeAdditionalProduct,
    ProductAdditionalProduct,
    FestivalPage,
    FestivalPageWebimage,
    FestivalPageProduct,
)


class ImageWebimageInline(admin.TabularInline):
    model = ImageWebimage
    fields = ('webimage', 'name', 'order', 'original_image',)
    extra = 1
    readonly_fields = ('original_image',)


class ProductWebimageInline(admin.TabularInline):
    model = ProductWebimage
    extra = 1


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1


class ImageGalleryInline(admin.TabularInline):
    model = ImageGallery
    extra = 1


class ProductAdditionalProductInline(admin.TabularInline):
    model = ProductAdditionalProduct
    fk_name = "product"
    extra = 0


class ImageAdmin(admin.ModelAdmin):
    inlines = [ImageWebimageInline, ProductInline, ImageGalleryInline]

    list_display = ['slug', 'title']


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductWebimageInline, ProductAdditionalProductInline]

    list_display = ['image', 'product_type', 'product_type_order']


class GalleryAdmin(admin.ModelAdmin):
    list_display = ['slug', 'name', 'parent', 'order']


class ImageGalleryAdmin(admin.ModelAdmin):
    list_display = ['image', 'gallery', 'order']


class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ['slug', 'title', 'parent', 'order']


class HomePageWebimageAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'enabled']

    exclude = ('sizes',)


class HolidayMessageAdmin(admin.ModelAdmin):
    list_display = ['start', 'end']


class ProductTypeAdditionalProductAdmin(admin.ModelAdmin):
    list_display = ['product_type', 'product']


class FestivalPageWebimageInline(admin.TabularInline):
    model = FestivalPageWebimage
    extra = 1

class FestivalPageProductInline(admin.TabularInline):
    model = FestivalPageProduct
    extra = 1

class FestivalPageAdmin(admin.ModelAdmin):
    inlines = [FestivalPageWebimageInline, FestivalPageProductInline]


admin.site.register(Image, ImageAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(ImageGallery, ImageGalleryAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(HomePageWebimage, HomePageWebimageAdmin)
admin.site.register(HolidayMessage, HolidayMessageAdmin)
admin.site.register(ProductTypeAdditionalProduct, ProductTypeAdditionalProductAdmin)
admin.site.register(FestivalPage, FestivalPageAdmin)
admin.site.register([ImageTag, ProductTag, PostagePrice])
