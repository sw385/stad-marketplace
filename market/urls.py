from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'), # nancy: index page
    path('user/<str:username>/products', views.Products, name='user-shop'),
    path('product/<uuid:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('product/create/', views.ProductCreate.as_view(), name='product-create'),
]
