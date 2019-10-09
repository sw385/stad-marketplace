# market/views.py
from django.shortcuts import render
from django.views import generic
from django.shortcuts import get_object_or_404
from users.models import CustomUser
from market.models import Product, Order, ShoppingCart, Category

from django.core.paginator import Paginator

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import View


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
'''    add paginate   '''
def Products(request, username):
    # If a user with the given username (from url) does not exist 404 error
    user = get_object_or_404(CustomUser, username = username)

    # User does exist, so get all of user's items for sale and put in context
    inventory = Product.objects.filter(seller = user)
    
    return render(request, 'market/product_list.html', context={'inventory': inventory, 'user': user})


# Page for each individual item
class ProductDetailView(generic.DetailView):
    model = Product
    
class ProductListView(generic.ListView):
    model = Product
    paginate_by = 4


# Page with a form for user to add a new product for sale.
# Redirects to the detail view for the new item
''' doesn't work yet - needs to set seller as the currently logged in user '''
class ProductCreate(CreateView):
    model = Product
    fields = ['name', 'price', 'description', 'quantity_available', 'category']
    '''
    def form_valid(self, form):
        product = form.save(commit=False)
        product.seller = User.objects.get(seller=self.request.seller)
        product.save()
        return HttpResponseRedirect(self.get_success_url())
    '''




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