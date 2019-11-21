# market/views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect 
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from market.models import Product, Order, ShoppingCart, Category
from users.models import CustomUser
from .forms import ProductForm


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_users = CustomUser.objects.count()
    num_products = Product.objects.count()
    num_orders = Order.objects.count()
    num_shoppingcarts = ShoppingCart.objects.count()
    num_categories = Category.objects.count()

    context = {
        'num_users' : num_users,
        'num_products' : num_products,
        'num_orders' : num_orders,
        'num_shoppingcarts' : num_shoppingcarts,
        'num_categories' : num_categories,   
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

# Page for each user which displays the products they have for sale
def Storefront(request, username):
    # If a user with the given username (from url) does not exist 404 error
    user = get_object_or_404(CustomUser, username = username)

    # User does exist, so get all of user's items for sale and put in context
    inventory = Product.objects.filter(seller = user)

    context = {
        'inventory': inventory, 
        'user': user,
        'logged_in_user': request.user
    }
    
    return render(request, 'market/user_storefront.html', context)


# Page for each individual item
def ProductDetailView(request, pk):
    product = get_object_or_404(Product, id=pk)
    
    context = {
        'product': product,
        'logged_in_user': request.user
    }

    return render(request, 'market/product_detail.html', context)


# Lists all products in the entire database
class ProductListView(generic.ListView):
    model = Product
    paginate_by = 4


# Should only be viewable if user is logged in
# The seller will automatically be set to the logged in user
@login_required
def NewProduct(request):
    if request.method == "POST":
        form = ProductForm(data=request.POST)

        if form.is_valid():
            new_product = form.save(commit=False)
            new_product.seller = request.user
            #new_product.published_date = timezone.now()
            new_product.save()
            form.save_m2m()
        
            return redirect('product-detail', new_product.id)
    else:
        form = ProductForm()
        
    return render(request, 'market/product_form.html', {'form': form})



@login_required
def DeleteProduct(request, pk):
    # if the product does not exist, 404 error
    product = get_object_or_404(Product, id=pk)

    # if the product's seller is not the user requesting to delete, 403 (forbidden) error
    if request.user != product.seller:
        raise PermissionDenied

    if request.method == 'POST':
        product.delete()
        return redirect('user-shop', request.user.username)
    
    return render(request, 'market/product_confirm_delete.html')


@login_required
def UpdateProduct(request, pk):
    # if item does not exist, 404 error
    product = get_object_or_404(Product, id=pk)

    # if the product's seller is not the user requesting to update, 403 (forbidden) error
    if request.user != product.seller:
        raise PermissionDenied


    # product does exist
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        form.save_m2m()
        return redirect('product-detail', product.id)    # redirect to product page instead
    
    return render(request, 'market/product_form.html', {'form': form}) 


# from django.views import generic

class OrderListView(generic.ListView):
    model = Order
    # context_object_name = 'my_book_list'   # your own name for the list as a template variable
    # queryset = Book.objects.filter(title__icontains='p')[:5] # Get 5 books containing the title war
    # queryset = Book.objects.order_by('title')
    # template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location
    paginate_by = 4
    
class OrderDetailView(generic.DetailView):
    model = Order
    
class ShoppingCartListView(generic.ListView):
    model = ShoppingCart
    # context_object_name = 'my_book_list'   # your own name for the list as a template variable
    # queryset = Book.objects.filter(title__icontains='p')[:5] # Get 5 books containing the title war
    # queryset = Book.objects.order_by('title')
    # template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location
    paginate_by = 4
    
class ShoppingCartDetailView(generic.DetailView):
    model = ShoppingCart

class UserListView(generic.ListView):
    model = CustomUser
    # context_object_name = 'my_book_list'   # your own name for the list as a template variable
    # queryset = Book.objects.filter(title__icontains='p')[:5] # Get 5 books containing the title war
    # queryset = Book.objects.order_by('title')
    # template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location
    paginate_by = 4
    
class UserDetailView(generic.DetailView):
    model = CustomUser
    
class CategoryListView(generic.ListView):
    model = Category
    # context_object_name = 'my_book_list'   # your own name for the list as a template variable
    # queryset = Book.objects.filter(title__icontains='p')[:5] # Get 5 books containing the title war
    # queryset = Book.objects.order_by('title')
    # template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location
    paginate_by = 4
    
class CategoryDetailView(generic.DetailView):
    model = Category