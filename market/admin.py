from django.contrib import admin
from market.models import Product, Category, Image, Order, OrderedProduct, ShoppingCart, ShoppingCartProduct

from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from market.forms import UserInfoCreationForm, UserInfoChangeForm
from market.models import UserInfo

class UserInfoAdmin(UserAdmin):
    add_form = UserInfoCreationForm
    form = UserInfoChangeForm
    model = UserInfo
    list_display = ['last_name', 'first_name', 'email', 'username',]

admin.site.register(UserInfo, UserInfoAdmin)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'seller', 'quantity_available', 'quantity_sold')

admin.site.register(Category)
admin.site.register(Image)

admin.site.register(Order)
admin.site.register(OrderedProduct)

admin.site.register(ShoppingCart)
admin.site.register(ShoppingCartProduct)


