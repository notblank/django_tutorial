from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode
from . import models

# Register your models here.

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']

    # preload related fields:
    list_select_related = ['collection']
    
    # To implement sorting for the new col:
    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'low'
        return 'ok'

    # retreive fields from related objects:
    def collection_title(self, product):
        return product.collection.title

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders']
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    list_per_page = 10

    # ??????????
    def orders(self, customer):
        return customer.orders_count

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
                orders_count=Count('order')
                )
    # Add column to view the orders of each customer 

#admin.site.register(models.Collection)
# instead of using decorator above:
#admin.site.register(models.Product, ProductAdmin)

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']
    ordering = ['placed_at']
    list_per_page = 10

# Overrinding base qSet:
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (
                reverse('admin:store_product_changelist')
                + '?'
                + urlencode({
                    'collection_id': str(collection.id)
                    }))
        return format_html('<a href={}>{}</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
                products_count=Count('product')
                )

