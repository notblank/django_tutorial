from django.db import models

class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()

class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', 
            on_delete=models.SET_NULL, 
            null=True, 
            #Dont want to get reverse rel to clash with collection in Product
            related_name='+') 
    # Overwrite to show titles in admin site:
    def __str__(self) -> str:
        return self.title

    # To sort collections by title in admin site:
    class Meta:
        ordering = ['title']

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion)

    # Admin site config:
    def __str__(self) -> str:
        return self.title
    class Meta:
        ordering = ['title']

class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    
    MEM_BRONZE = 'B'
    MEM_SILVER = 'S'
    MEM_GOLD = 'G'

    MEM_CHOICES = [
            (MEM_BRONZE, 'Bronze'),
            (MEM_SILVER, 'Silver'),
            (MEM_GOLD, 'Gold')
            ]
    membership = models.CharField(max_length=1, 
            choices=MEM_CHOICES, default=MEM_BRONZE)
   
    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ['last_name', 'first_name']

class Order(models.Model):
    placed_at = models.DateTimeField(auto_now_add=True)

    P_STAT_PEND = 'P'
    P_STAT_COMPL = 'C'
    P_STAT_FAIL = 'F'
    P_STAT_CHOICES = [
            (P_STAT_PEND, 'Pending'),
            (P_STAT_COMPL, 'Complete'),
            (P_STAT_FAIL, 'Failed')
            ]
    payment_status = models.CharField(max_length=1, 
            choices=P_STAT_CHOICES, default=P_STAT_PEND)
    customer=models.ForeignKey(Customer, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.placed_at

    
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    zip_code = models.PositiveIntegerField()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


