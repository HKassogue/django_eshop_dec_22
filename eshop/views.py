from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Category
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count


# Create your views here.
def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context =  {
        'products': products,
        'categories': categories
    }
    return render(request, "eshop/index.html", context)

def shop(request, cat='all'):
    categories = Category.objects.all()
    total = sum([category.products.count() for category in categories])
    page = request.GET.get('page', 1)
    perpage = request.GET.get('per', 6)
    sort = request.GET.get('sort', 'latest')
    query = request.GET.get('q', '')

    if cat == 'all':
        if not query:
            if sort == 'latest':
                products = Product.objects.all()
            elif sort == 'popular':
                products = Product.objects.all().annotate(nbr_likes=Count('likes')).order_by('-nbr_likes')
            else:
                products = Product.objects.all().annotate(nbr_reviews=Count('reviews__rate')).order_by('-nbr_reviews')
        else:
            products = Product.objects.filter(name__icontains=query)
    else:
        if not query:
            if sort == 'latest':
                products = Product.objects.filter(category__slug=cat)
            elif sort == 'popular':
                products = Product.objects.filter(category__slug=cat).annotate(nbr_likes=Count('likes')).order_by('-nbr_likes')
            else:
                products = Product.objects.filter(category__slug=cat).annotate(nbr_reviews=Count('reviews__rate')).order_by('-nbr_reviews')
        else:
            products = Product.objects.filter(category__slug=cat).filter(name__icontains=query)

    paginator = Paginator(products, perpage)
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


def search(request):
    query = request.GET.get('q', '')
    if not query:
        return redirect('shop')

    page = request.GET.get('page', 1)
    perpage = request.GET.get('per', 6)
    products = Product.objects.filter(name__icontains=query)
    categories = Category.objects.all()

    paginator = Paginator(products, perpage)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
         'products' : products,
         'categories' :categories,
    }
    return render(request,"eshop/shop.html", context)


def detail(request, id):
    product = Product.objects.get(id=id)
    categories = Category.objects.all()
    sim_products = Product.objects.filter(category=product.category).filter(active=True)

    context =  {
        'product': product,
        'categories': categories,
        'sim_products': sim_products,
    }
    return render(request,"eshop/detail.html", context)

def contact(request):
    return render(request,"eshop/contact.html", {})

def cart(request):
    return render(request,"eshop/cart.html", {})

def checkout(request):
    return render(request,"eshop/checkout.html", {})

def login(request):
    return render(request, "eshop/login.html")