from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode
from . import models

# Register your models here.

# Custom filters:
class InventoryFilter(admin.SimpleListFilter):
    title = 'stock'
    # because we want inventory < 10 to be low:
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
                ('<10', 'Low'),
                ('>10', 'Normal')
                ]

    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        else:
            return queryset.filter(inventory__gte=10)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']

    # preload related fields:
    list_select_related = ['collection']

    # filters
    list_filter = ['collection', 'last_update', InventoryFilter]
    
    # To implement sorting for the new col:
    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'low'
        return 'ok'

    # retreive fields from related objects:
    def collection_title(self, product):
        return product.collection.title

    # Custom Actions:
    actions = ['clear_inventory']
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
                request, 
                f'{updated_count} products were successfully updated'
                )

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    # define the orders field:
    @admin.display(ordering='orders_count')
    def orders(self, customer):
        # urls with filters are formated:
        # /model_changelist?query
        url = (
                reverse('admin:store_order_changelist')
                + '?'
                + urlencode({
                    'customer_id': str(customer.id)
                    }))
        return format_html('<a href={}>{}</a>', url, customer.orders_count)
        #return customer.orders_count

    # add the orders count col in customer:
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
                orders_count=Count('order')
                )

#admin.site.register(models.Collection)
# instead of using decorator above:
#admin.site.register(models.Product, ProductAdmin)

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']
    ordering = ['placed_at']
    list_per_page = 10

    # When adding customer, customer field is autocomplete:
    autocomplete_fields = ['customer']

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

