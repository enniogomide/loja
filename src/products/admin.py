from django.contrib import admin
from . import models


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'quantity', 'price',]
    list_filter = ['name',]
    search_fields = ['name',]
    list_per_page = 20


admin.site.register(models.Product, ProductAdmin)