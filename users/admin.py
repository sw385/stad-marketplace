# users/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
	add_form = CustomUserCreationForm
	form = CustomUserChangeForm
	model = CustomUser
	list_display = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'last_login']
	fieldsets = UserAdmin.fieldsets + (
			(None, {'fields': ('date_of_birth', 'phone', 'address', 'state', 'city', 'zip_code', 'payment_method', 'order_seller', 'order_buyer')}),
	)


admin.site.register(CustomUser, CustomUserAdmin)