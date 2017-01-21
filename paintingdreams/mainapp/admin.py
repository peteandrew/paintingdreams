from django.contrib import admin
from mainapp.models import Image, ImageWebimage, ProductType, ImageTag, ImageImageTag, ProductTag, Product, ProductWebimage, PostagePrice


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


class ImageImageTagInline(admin.TabularInline):
    model = ImageImageTag
    extra = 1


class ImageAdmin(admin.ModelAdmin):
    inlines = [ImageWebimageInline, ProductInline, ImageImageTagInline]

    list_display = ['slug', 'title']


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductWebimageInline]

    list_display = ['image', 'product_type', 'product_type_order']


class ImageTagAdmin(admin.ModelAdmin):
    list_display = ['slug', 'name', 'parent', 'order']


class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ['slug', 'title', 'parent', 'order']


admin.site.register(Image, ImageAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ImageTag, ImageTagAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register([ImageImageTag, ProductTag, PostagePrice])
