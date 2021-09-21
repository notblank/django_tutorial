from django.shortcuts import render
from django.http import HttpResponse 
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Max, Min, Sum
from django.db.models.functions import Least 
from django.contrib.contenttypes.models import ContentType
from store.models import Product, Customer, Order, OrderItem, Collection, \
        Cart, CartItem
from tags.models import TaggedItem

# Create your views here.
def say_hello(request):

    #try:
    #    prod_1 = Product.objects.get(pk=0)
    #except ObjectDoesNotExist:
    #    pass    

    #could use instead:
    #prod_0 = Product.objects.filter(pk=0).first()

    #q_set:
    #q_set = Product.objects.all()
    # to querry:
    #for prod in q_set:
        #print(prod)

    #filter:
    #q_set_filter = Product.objects.filter(unit_price__range=(20, 30))

    # Exercises:
    #q1 = Customer.objects.filter(email__icontains='.com')

    #Selecting Fields:
    #q_s = Product.objects.values('id', 'title', 'collection__title')

    # select ordered products and order by title:
    q_op = OrderItem.objects.values('unit_price', 'product__title').order_by('product__title')

    #Deffering Fields:
    #q_d = Product.objects.only('id', 'title')

    #Related Objects:
    #q_ro = Product.objects.select_related('collection').all()
    #For many-to-many use:
    #q_mm = Product.objects.prefetch_related('promotions').all().order_by('title', 'description')
    # Get last 5 orders with their customers and items:
    # Recall the django creates reverse relationships denoted name_set:
    #q_oc = Order.objects.select_related('customer')\
    #                .prefetch_related('orderitem_set__product')\
    #                .order_by('-placed_at')[:5]

    # Aggregates:
    #q_no = Order.objects.aggregate(Count('id'))

    #Annotations:
    #q_customers_last_order = Customer.objects\
    #        .annotate(last_order = Max('order__placed_at'))

    #q_collections_prod_counts = Collection.objects\
    #        .annotate(prod_count=Count('product__collection_id'))

    #q_customer_total_spent = Order.objects\
    #        .values('customer__first_name')\
    #        .annotate(total_orders=Sum('orderitem__unit_price'))

    # Query Generic Rel:
    content_type = ContentType.objects.get_for_model(Product)
    q_tags = TaggedItem.objects.get_tags_for(Product, 1)

    # Inserting objects into a database
    #collection = Collection()
    #collection.title = 'Video Games'
    #collection.featured_product_id = '1'
    #collection.save()
    
    # Exercises:
    # A cart with an item
    #cart = Cart()
    #cart.save()
    #item1 = CartItem()
    #item1.cart = cart
    #item1.product_id = 1
    #item1.quantity = 1
    #item1.save()

    # Update an item in a shopping cart
    #item = CartItem.objects.get(cart_id=4)
    #item.quantity=4
    #item.save()
    
    # Remove a shopping cart with its items:
    # deleting the cart cascades into the items
    #Cart.objects.get(pk=6).delete()

    return(render(request, 'hello.html', 
        { 'name': 'Fede', 'results': list(q_tags) }))
     

