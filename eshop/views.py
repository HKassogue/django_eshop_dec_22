from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Category
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.
def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context =  {
        'products': products,
        'categories': categories
    }
    return render(request, "eshop/index.html", context)

def shop(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    total = sum([category.products.count() for category in categories])
    page = request.GET.get('page', 1)

    paginator = Paginator(products, 6)
    try:
        produit = paginator.page(page)
    except PageNotAnInteger:
        produit = paginator.page(1)
    except EmptyPage:
        produit = paginator.page(paginator.num_pages)

    context = {
         'products' : produit,
         'categories' :categories,
         'total': total
    }
    return render(request,"eshop/shop.html", context)

def detail(request, id):
    product = Product.objects.get(id=id)
    categories = Category.objects.all()
    context =  {
        'product': product,
        'categories': categories
    }
    return render(request,"eshop/detail.html", context)

def contact(request):
    return render(request,"eshop/contact.html", {})

def cart(request):
    return render(request,"eshop/cart.html", {})

def checkout(request):
    return render(request,"eshop/checkout.html", {})