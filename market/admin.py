from django.contrib import admin
from market.models import Product, Category, Image, Order, OrderedProduct, User


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Image)

admin.site.register(Order)
admin.site.register(OrderedProduct)

# admin.site.register(User)

class UserAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'username', 'email')

admin.site.register(User, UserAdmin)