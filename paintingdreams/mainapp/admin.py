from django.contrib import admin
from mainapp.models import (
    Image,
    ImageTag,
    ImageWebimage,
    ProductType,
    Gallery,
    ImageGallery,
    NewProduct,
    ProductTag,
    Product,
    ProductWebimage,
    PostagePrice,
    HomePageWebimage,
    FeedbackWebimage,
    HolidayMessage,
    ProductTypeAdditionalProduct,
    ProductTypeDestinationShippingWeightOverride,
    ProductAdditionalProduct,
    FestivalPage,
    FestivalPageWebimage,
    FestivalPageProduct,
    DiscountCode,
    DiscountCodeProduct,
    HomePageProduct,
    Feedback,
    FeedbackProduct,
)


class ImageWebimageInline(admin.TabularInline):
    model = ImageWebimage
    fields = ('webimage', 'name', 'order', 'original_image',)
    extra = 1
    readonly_fields = ('original_image',)


class ProductWebimageInline(admin.TabularInline):
    model = ProductWebimage
    fields = ('webimage', 'name', 'order', 'original_image',)
    extra = 1
    readonly_fields = ('original_image',)


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
    search_fields = ['title']


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductWebimageInline, ProductAdditionalProductInline]

    list_display = ['image', 'product_type', 'product_type_order']
    search_fields = ['image__title', 'product_type__title']


class GalleryAdmin(admin.ModelAdmin):
    list_display = ['slug', 'name', 'parent', 'order']
 

class ImageGalleryAdmin(admin.ModelAdmin):
    list_display = ['image', 'gallery', 'order']
    search_fields = ['image__title', 'gallery__name']


class ProductTypeDestinationShippingWeightOverrideInline(admin.TabularInline):
    model = ProductTypeDestinationShippingWeightOverride
    extra = 0


class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [ProductTypeDestinationShippingWeightOverrideInline]

    list_display = ['slug', 'title', 'parent', 'order']
    search_fields = ['title']


class HomePageWebimageAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'enabled']

    exclude = ('sizes',)


class HolidayMessageAdmin(admin.ModelAdmin):
    list_display = ['start', 'end']


class ProductTypeAdditionalProductAdmin(admin.ModelAdmin):
    list_display = ['product_type', 'product']


class FestivalPageWebimageInline(admin.TabularInline):
    model = FestivalPageWebimage
    fields = ('webimage', 'name', 'order', 'original_image',)
    extra = 1
    readonly_fields = ('original_image',)


class FestivalPageProductInline(admin.TabularInline):
    model = FestivalPageProduct
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        field = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == "product" and hasattr(self, "cached_products"):
            field.choices = self.cached_products
        return field


class FestivalPageAdmin(admin.ModelAdmin):
    inlines = [FestivalPageWebimageInline, FestivalPageProductInline]

    def get_formsets_with_inlines(self, request, obj=None):
        cached_products = [('', '---------',)] + [(i.pk, str(i)) for i in Product.objects.all()]
        for inline in self.get_inline_instances(request, obj):
            if inline.model == FestivalPageProduct:
                inline.cached_products = cached_products
            yield inline.get_formset(request, obj), inline


class DiscountCodeProductInline(admin.TabularInline):
    model = DiscountCodeProduct
    extra = 1


class DiscountCodeAdmin(admin.ModelAdmin):
    inlines = [DiscountCodeProductInline]
    list_display = ['code']


class HomePageProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'order']


class NewProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'order']


class FeedbackWebimageInline(admin.TabularInline):
    model = FeedbackWebimage
    fields = ('webimage', 'name', 'order', 'original_image',)
    extra = 1
    readonly_fields = ('original_image',)


class FeedbackProductInline(admin.TabularInline):
    model = FeedbackProduct
    extra = 0


class FeedbackAdmin(admin.ModelAdmin):
    inlines = [FeedbackWebimageInline, FeedbackProductInline]
    fields = ('feedback', 'author_name', 'author_email', 'created', 'show_date')
    list_display = ['created']


admin.site.register(Image, ImageAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(ImageGallery, ImageGalleryAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(HomePageWebimage, HomePageWebimageAdmin)
admin.site.register(HolidayMessage, HolidayMessageAdmin)
admin.site.register(ProductTypeAdditionalProduct, ProductTypeAdditionalProductAdmin)
admin.site.register(FestivalPage, FestivalPageAdmin)
admin.site.register(DiscountCode, DiscountCodeAdmin)
admin.site.register(HomePageProduct, HomePageProductAdmin)
admin.site.register(NewProduct, NewProductAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register([ImageTag, ProductTag, PostagePrice])