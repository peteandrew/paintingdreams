from django.contrib import admin
from mainapp.models import Image, ImageWebimage, ProductType, ImageTag, ProductTag, Product, ProductWebimage, PostagePrice


class ImageWebimageInline(admin.TabularInline):
    model = ImageWebimage
    extra = 1
    readonly_fields = ('original_image',)


class ProductWebimageInline(admin.TabularInline):
    model = ProductWebimage
    extra = 1


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1


class ImageAdmin(admin.ModelAdmin):
    inlines = [ImageWebimageInline, ProductInline]

    list_display = ['slug', 'title']


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductWebimageInline]

    list_display = ['image', 'product_type']


admin.site.register(Image, ImageAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register([ProductType, ImageTag, ProductTag, PostagePrice])
