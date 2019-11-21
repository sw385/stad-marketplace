# market/urls.py
from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),

    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('product/<uuid:pk>/', views.ProductDetailView, name='product-detail'),
    path('product/create/', views.NewProduct, name='product-create'),
    path('product/<uuid:pk>/update/', views.UpdateProduct, name='product-update'),
    path('product/<uuid:pk>/delete/', views.DeleteProduct, name='product-delete'),
    path('user/<str:username>/products', views.Storefront, name='user-shop'),

    path('orders/', views.OrderListView.as_view(), name='order-list'),
    path('order/<uuid:pk>', views.OrderDetailView.as_view(), name='order-detail'),
    
    path('shoppingcarts/', views.ShoppingCartListView.as_view(), name='shoppingcart-list'),
    path('shoppingcart/<str:pk>', views.ShoppingCartDetailView.as_view(), name='shoppingcart-detail'),
    
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('user/<str:pk>', views.UserDetailView.as_view(), name='user-detail'),
    
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('category/<str:pk>', views.CategoryDetailView.as_view(), name='category-detail'),
]
