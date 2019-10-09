# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
	date_of_birth = models.DateField(null=True, blank=True) #2019-10-31
	phone = models.CharField(max_length=10, unique=True)
	address = models.CharField(max_length=255)
	state = models.CharField(max_length=30)
	city = models.CharField(max_length=30)
	zip_code = models.CharField(max_length=10)
	payment_method = models.CharField(max_length=16, default='None')
	order_seller = models.CharField(max_length=100, default='None')
	order_buyer = models.CharField(max_length=100, default='None')

	def __str__(self):
		return self.email