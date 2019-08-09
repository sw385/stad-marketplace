from django.db import models
from datetime import date
from PIL import Image


class Category(models.Model):
 	name = models.CharField(max_length = 30, help_text = 'Enter a name for this category.')
 	
 	class Meta:
 		verbose_name_plural = 'categories'

 	def __str__(self):
 		return f'{self.name}'


class Product(models.Model):
	name = models.CharField(max_length = 50)
	
	#seller = models.ForeignKey(User)

	#pictures = models.ManyToManyField(Image, help_text = 'Select some pictures for this product.')

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


class Image(models.Model):
	description = models.CharField(max_length = 35, help_text = 'Enter a description for this image.')
	
	image = models.ImageField(upload_to = './pictures/') 
	#uploaded_by = models.ForeignKey(User) #when user is deleted delete all of their pictures?

	def __str__(self):
		return f'{self.id}'	
