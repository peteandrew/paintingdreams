from django.contrib import admin
from wholesale.models import Category, Product, Special, SpecialProductRemoved

class ProductAdmin(admin.ModelAdmin):
    list_display = ['code', 'title']


admin.site.register(Product, ProductAdmin)
admin.site.register([Category, Special, SpecialProductRemoved])
