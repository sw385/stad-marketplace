from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import uuid # Reguired for unique id

# Create your models here.

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

	def get_absoulte_url(self):
		"""Returns the url to access a particular instances of the model. """
		return reverse('user-detail-view', args=[str(self.id)])

