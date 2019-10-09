# market/admin.py
from django.contrib import admin
from market.models import Product, Category, Image, Order, OrderedProduct, ShoppingCart, ShoppingCartProduct

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'seller', 'quantity_available', 'quantity_sold')

admin.site.register(Category)
admin.site.register(Image)

admin.site.register(Order)
admin.site.register(OrderedProduct)

admin.site.register(ShoppingCart)
admin.site.register(ShoppingCartProduct)


