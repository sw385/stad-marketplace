from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'), # nancy: index page
    path('user/<str:username>/products', views.Products, name='user-shop'),
    path('product/<uuid:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('product/create/', views.ProductCreate.as_view(), name='product-create'),
    path('products/', views.ProductListView.as_view(), name='product-list'),
    
    
    # path('authors/', views.AuthorListView.as_view(), name='authors-list'),
    # path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    
    path('orders/', views.OrderListView.as_view(), name='order-list'),
    path('order/<uuid:pk>', views.OrderDetailView.as_view(), name='order-detail'),
    
    path('shoppingcarts/', views.ShoppingCartListView.as_view(), name='shoppingcart-list'),
    path('shoppingcart/<uuid:pk>', views.ShoppingCartDetailView.as_view(), name='shoppingcart-detail'),
    
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('user/<str:pk>', views.UserDetailView.as_view(), name='user-detail'),
    
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('category/<str:pk>', views.CategoryDetailView.as_view(), name='category-detail'),
]
