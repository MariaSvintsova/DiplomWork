from django.contrib import admin

from products.models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at',)
    list_filter = ('name', 'price', 'is_active',)