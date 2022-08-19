import django
from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm
from .models import Category, Product
from .recommender import Recommender
from django.views.generic import ListView
from django.db.models import Q

# Create your views here.
def product_list(request,category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available = True)
    if category_slug:
        category = get_object_or_404(Category,slug = category_slug)
        products = products.filter(category=category)
    return render(request,'shop/product/list.html',{'category':category,'categories':categories,'products':products})

def product_detail(request,id,slug):
    product = get_object_or_404(Product,id=id,slug=slug,available=True)
    cart_product_form = CartAddProductForm()
    r = Recommender()
    recommended_products = r.suggest_products_for([product],4)
    return render(request,'shop/product/detail.html',{'product':product,'cart_product_form':cart_product_form,'recommended_products':recommended_products})

def base_view(request):
    categories = Category.objects.all()
    return render(request,'shop/base.html',{'categories':categories})

def product_store(request):
    categories = Category.objects.all()
    min_price = request.GET.get('min_price',0)
    max_price = request.GET.get('max_price',10000000000)
    products = Product.objects.filter(price__range=(min_price,max_price))
    return render(request,'shop/product/store.html',{'categories':categories,'products':products})

class SearchResultsListView(ListView):
    model = Product
    context_object_name = 'result'
    template_name = 'shop/product/search_results.html'
    def get_queryset(self):
       query = self.request.GET.get('q')
       return Product.objects.filter(
        Q(name__icontains=query))
    
    
