# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'date_of_birth', 'phone', 
        	'address', 'state', 'city', 'zip_code')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'date_of_birth', 'phone', 
        	'address', 'state', 'city', 'zip_code',
        	'payment_method', 'order_seller', 'order_buyer')