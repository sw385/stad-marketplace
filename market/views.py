from django.shortcuts import render
from django.views import generic
from django.shortcuts import get_object_or_404
from market.models import Product, User

from django.core.paginator import Paginator

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import View

# nancy: index page for showing number of products and vendors
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_users = User.objects.count()
    #num_products = Product.objects.all.count()
    #num_vendors =

    context = {
        'num_users' : num_users,
        #'num_products' : num_products,
    }


    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

# Page for each user which displays the products they have for sale
'''    add paginate   '''
def Products(request, username):
    # If a user with the given username (from url) does not exist 404 error
    user = get_object_or_404(User, username = username)

    # User does exist, so get all of user's items for sale and put in context
    inventory = Product.objects.filter(seller = user)
    
    return render(request, 'market/product_list.html', context={'inventory': inventory, 'user': user})


# Page for each individual item
class ProductDetailView(generic.DetailView):
    model = Product


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
