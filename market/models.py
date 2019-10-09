# market/models.py
from django.db import models
from users.models import CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
from PIL import Image
from django.urls import reverse
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator

class Category(models.Model):
    name = models.CharField(primary_key=True, max_length=30, unique=True, help_text='Enter a name for this category.')
     
    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'
        
    def get_absolute_url(self):
        """Returns the url to access a particular instances of the model. """
        return reverse('category-detail', args=[str(self.name)])


class Product(models.Model):
    name = models.CharField(max_length = 50)
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='The unique ID for this product.')
    #on_delete = models.CASCADE,
    seller = models.ForeignKey(CustomUser, on_delete = models.CASCADE, null=False)

    # The price of the product must be between $0.01 and $99,999.99
    price = models.DecimalField(
        max_digits = 7,
        decimal_places = 2,
        help_text = 'Enter the price of this product.',
        validators = [
            MinValueValidator(0.01),
            MaxValueValidator(99999.99),
        ]
    )
    
    description = models.TextField(max_length = 2500, help_text = 'Enter a description for this product.')

    # The quantity must be 1 or more
    quantity_available = models.PositiveIntegerField(
        validators = [
            MinValueValidator(1),
            MaxValueValidator(999),
        ]
    )

    # The number of this product sold since it was listed
    # Should not be editable by the user
    quantity_sold = models.IntegerField(default=0)

    # One product can have multiple categories
    category = models.ManyToManyField(Category, help_text = 'Enter a category for this product.')

    # The time and date the item was added at
    added_at = models.DateTimeField(auto_now_add = True)

    # The time and date when the item was last updated
    last_updated = models.DateTimeField(auto_now = True)

    # Items that still have viewable pages but are no longer for sale are marked as delisted.
    delisted = models.BooleanField(default = False, help_text = 'Delisting an item marks it as no longer available.')
    
    class Meta:
        ordering = ['-last_updated']

    def get_absolute_url(self):
        return reverse('product-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.name} sold by {self.seller}'


class Image(models.Model):
    description = models.CharField(max_length = 35, help_text = 'Enter a description for this image.')
    
    image = models.ImageField(upload_to = './pictures/') 
    uploaded_by = models.ForeignKey(CustomUser, on_delete = models.CASCADE, null=True) #when user is deleted delete all of their pictures
    product = models.ForeignKey(Product, on_delete = models.CASCADE, null=True)

    def __str__(self):
        return f'{self.id}'   
        


class Order(models.Model):
    # id = models.AutoField(primary_key=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text='Unique order number')
        
    # time and date the order was submitted
    date_ordered = models.DateTimeField(auto_now_add = True)
    
    # ForeignKey of the buyer
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    
    # the fields in Order should not be directly editable, but they should be for development
    subtotal = models.DecimalField(
        max_digits = 6,
        decimal_places = 2,
        help_text = 'Enter the subtotal for this order.',
        # editable = False,
        default = 0,
    )
        
    tax = models.DecimalField(
        max_digits = 6,
        decimal_places = 2,
        help_text = 'Enter the tax for this order.',
        # editable = False,
        default = 0,
    )
        
    # shipping address
    address = models.CharField(max_length=255, default='')
    city = models.CharField(max_length=30, default='')
    state = models.CharField(max_length=30, default='')
    zip_code = models.CharField(max_length=10, default='')
    # payment method
    payment_method = models.CharField(max_length=16, default='')
    # billing address is unimplemented, will probably be similar to shipping address
    
    class Meta:
        # order with the most recent orders first
        ordering = ['-date_ordered']
    
    def __str__(self):
        return f'{self.id}'
        
    def get_absolute_url(self):
        """Returns the url to access a particular instances of the model. """
        return reverse('order-detail', args=[str(self.id)])


class OrderedProduct(models.Model):
    # id = models.AutoField(primary_key=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text='Unique ID for an ordered product')
    
    # Order ID of the order this product is in
    containing_order = models.ForeignKey(Order, on_delete=models.CASCADE)
    # It might make more sense to prevent the deletion of orders and products, but give them a field to prevent them from showing up in search results. That way, orders containing those products can still access the information about the product.
        
    # Product ID (the Order ID and Product ID together form a unique composite key)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
        
    # quantity of the product ordered, must be at least 1, maximum is 100
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
        
    # price at time of order, not edited directly by users
    price = models.DecimalField(
        max_digits = 6,
        decimal_places = 2,
        help_text = 'Enter the price of this product.',
        # editable = False,
    )

    ITEM_STATUS = (
        ('p', 'Order placed'),
        ('r', 'Order received'),
        # ('c', 'Payment confirmed'),
        ('s', 'Shipped'),
        ('d', 'Delivered'),
    )

    status = models.CharField(
        max_length=1,
        choices=ITEM_STATUS,
        blank=False,
        default='p',
        help_text='The fulfillment status of a particular item.',
    )

    def __str__(self):
        # return the name of the product and quantity
        return f'{self.product}: {self.quantity}'
        


class ShoppingCart(models.Model):
    # ShoppingCart and ShoppingCartProduct are similar to Order and OrderedProduct
    # except that the id of the ShoppingCart corresponds to the buyer/creator of the order
    # so that there is only one ShoppingCart associated with each user
    # and ShoppingCartProduct does not keep track of the status of each product, since the order hasn't been placed

    # the id of each ShoppingCart should be associated with a particular user
    # id = models.AutoField(primary_key=True)
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text='Unique order number')
    # ForeignKey of the buyer
    # market.ShoppingCart.buyer: (fields.W342) Setting unique=True on a ForeignKey has the same effect as using a OneToOneField.
        # HINT: ForeignKey(unique=True) is usually better served by a OneToOneField.
    # buyer = models.ForeignKey(User, primary_key=True, on_delete=models.CASCADE, null=False, default='NONE')
    buyer = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, null=False)
        
    # time and date the order was submitted
    date_ordered = models.DateTimeField(auto_now_add = True)
    
    # the fields in Order should not be directly editable, but they should be for development
    subtotal = models.DecimalField(
        max_digits = 6,
        decimal_places = 2,
        help_text = 'Enter the subtotal for this order.',
        # editable = False,
        default = 0,
    )
        
    tax = models.DecimalField(
        max_digits = 6,
        decimal_places = 2,
        help_text = 'Enter the tax for this order.',
        # editable = False,
        default = 0,
    )
        
    # shipping address
    address = models.CharField(max_length=255, default='')
    city = models.CharField(max_length=30, default='')
    state = models.CharField(max_length=30, default='')
    zip_code = models.CharField(max_length=10, default='')
    # payment method
    payment_method = models.CharField(max_length=16, default='')
    # billing address is unimplemented, will probably be similar to shipping address
    
    def __str__(self):
        return f'{self.buyer}'
        
    def get_absolute_url(self):
        """Returns the url to access a particular instances of the model. """
        return reverse('shoppingcart-detail', args=[str(self.buyer)])


class ShoppingCartProduct(models.Model):
    # id = models.AutoField(primary_key=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text='Unique ID for an ordered product')
    
    # Order ID of the cart this product is in
    containing_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    # It might make more sense to prevent the deletion of orders and products, but give them a field to prevent them from showing up in search results. That way, orders containing those products can still access the information about the product.
        
    # Product ID (the Order ID and Product ID together form a unique composite key)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
        
    # quantity of the product ordered, must be at least 1, maximum is 100
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
        
    # price at time of order, not edited directly by users
    price = models.DecimalField(
        max_digits = 6,
        decimal_places = 2,
        help_text = 'Enter the price of this product.',
        # editable = False,
    )
    
    # time and date the item was added to the shopping cart
    date_added = models.DateTimeField(auto_now_add = True)
    
    # We could order the items in the shopping cart in the order they were added, newest first
    # We'll need a field to keep track of the DateTime when the item was added
    class Meta:
        # order with the most recently added items first
        ordering = ['-date_added']

    def __str__(self):
        # return the name of the product and quantity
        return f'{self.product}: {self.quantity}'

