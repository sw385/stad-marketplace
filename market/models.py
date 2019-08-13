from django.db import models
from datetime import date
from PIL import Image

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import uuid # Required for unique id

from django.core.validators import MaxValueValidator, MinValueValidator


class User(AbstractBaseUser):
    # Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID')
    username = models.CharField(max_length=25)
    USERNAME_FIELD = 'username'
    #password =
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=10)
    payment_method = models.CharField(max_length=15, default='None')
    order_seller = models.CharField(max_length=100, default='None')
    order_buyer = models.CharField(max_length=100, default='None')

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # Meta
    class Meta:
        ordering = ['first_name', 'last_name']

    # Method
    def __str__(self):
        return f'{self.username}, {self.last_name} {self.first_name}'

    def get_absolute_url(self):
        """Returns the url to access a particular instances of the model. """
        return reverse('user-detail-view', args=[str(self.id)])

class Category(models.Model):
     name = models.CharField(max_length = 30, help_text = 'Enter a name for this category.')
     
     class Meta:
         verbose_name_plural = 'categories'

     def __str__(self):
         return f'{self.name}'


class Image(models.Model):
    description = models.CharField(max_length = 35, help_text = 'Enter a description for this image.')
    
    image = models.ImageField(upload_to = './pictures/') 
    uploaded_by = models.ForeignKey(User, on_delete = models.CASCADE, null=True) #when user is deleted delete all of their pictures?

    def __str__(self):
        return f'{self.id}'    


class Product(models.Model):
    name = models.CharField(max_length = 50)
    
    seller = models.ForeignKey(User, on_delete = models.CASCADE, null=True)

    pictures = models.ManyToManyField(Image, help_text = 'Select some pictures for this product.')

    # The price of the product must be between $0.01 and $9,999.99
    price = models.DecimalField(
        max_digits = 6,
        decimal_places = 2,
        help_text = 'Enter the price of this product.'
    )
    
    description = models.TextField(max_length = 2500, help_text = 'Enter a description for this product.')

    # The quantity must be 0 or more
    quantity_available = models.IntegerField()

    # The number of this product sold since it was listed
    # Should not be editable by the user
    quantity_sold = models.IntegerField(default=0)

    # One product can have multiple categories
    category = models.ManyToManyField(Category, help_text = 'Enter a category for this product.')

    # The time and date the item was added at
    added_at = models.DateTimeField(auto_now_add = True)

    # The time and date when the item was last updated
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product_name} {self.price} {self.quantity}'


class Order(models.Model):
    # id = models.AutoField(primary_key=True)
        
    # time and date the order was submitted
    date_ordered = models.DateTimeField(auto_now_add = True)
        
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
        
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
    state = models.CharField(max_length=30, default='')
    city = models.CharField(max_length=30, default='')
    zip_code = models.CharField(max_length=10, default='')
    # payment method
    payment_method = models.CharField(max_length=15, default='')
    # billing address is unimplemented, will probably be similar to shipping address
    
    def __str__(self):
        return f'{self.id}'    


class OrderedProduct(models.Model):
    # id = models.AutoField(primary_key=True)
    
    # Order ID of the order this product is in
    containing_order = models.ForeignKey(Order, on_delete=models.CASCADE)
        
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

    def __str__(self):
        # return the name of the product and quantity
        return f'{self.product}: {self.quantity}'
        


