from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Category

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
    return render(request, "eshop/shop.html", {})

def detail(request):
    return render(request,"eshop/detail.html", {})

def contact(request):
    return render(request,"eshop/contact.html", {})

def cart(request):
    return render(request,"eshop/cart.html", {})

def checkout(request):
    return render(request,"eshop/checkout.html", {})