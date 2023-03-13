from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from eshop.forms import CheckOutForm
from .models import Delivery, Payments, Product, Category, Order, Order_details, Customer
from.context_processors import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def index(request):
    products = Product.objects.all()
    context =  {
        'products': products,
    }

    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(user=request.user)
            order = Order.objects.get(customer=customer, completed=False)
            if order:
                order_details = Order_details.filter(order=order)
                cart = request.session.get('cart', {})
                for item in order_details:
                    key = str(item.product.id)
                    if key in cart:
                        cart[key] += item.quantity
                    else:
                        cart[key] = item.quantity
                request.session['cart'] = cart
                request.session.modified = True
        except ObjectDoesNotExist:
            pass

    return render(request, "eshop/index.html", context)

def shop(request, cat='all'):
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
    }
    return render(request,"eshop/shop.html", context)


def search(request):
    query = request.GET.get('q', '')
    if not query:
        return redirect('shop')

    page = request.GET.get('page', 1)
    perpage = request.GET.get('per', 6)
    products = Product.objects.filter(name__icontains=query)

    paginator = Paginator(products, perpage)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
         'products' : products,
    }
    return render(request,"eshop/shop.html", context)


def detail(request, id):
    product = Product.objects.get(id=id)
    sim_products = Product.objects.filter(category=product.category).filter(active=True)

    context =  {
        'product': product,
        'sim_products': sim_products,
    }
    return render(request,"eshop/detail.html", context)

def contact(request):
    return render(request,"eshop/contact.html", {})

def cart(request):
    cart = request.session.get('cart', {})
    products = []
    quantities = []
    total = 0
    shipping = 10
    coupon = 0
    for id, qty in cart.items():
        product = Product.objects.get(id=int(id))
        products.append(product)
        quantities.append(qty)
        total += qty * product.price
    return render(request,"eshop/cart.html", {'items': zip(products, quantities), 'total': total, 'shipping': shipping, 'coupon': coupon})

def checkout(request):
    # if request.user.is_authenticated:
    #     customer = Customer.objects.get(user=request.user)
    #     order = Order.objects.get(customer=customer, completed=False)
    if request.POST == 'POST':
        #order = Order.objects.get(customer=customer, completed=False)
        token = request.POST.get('stripeToken')
        #chargeID = stripe_payment(settings.STRIPE_SECRET_KEY,token, order.get_total(),str(order.id))
        form = CheckOutForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data.get('address')
            mobile = form.cleaned_data.get('mobile')
            country = form.cleaned_data.get('country')
            city = form.cleaned_data.get('city')
            state = form.cleaned_data.get('state')
            zipcode = form.cleaned_data.get('zipcode')
            delivery = Delivery(
                address = address,
                mobile = mobile,
                country = country,
                city = city,
                price = 0,
                delivery_by = "",
                state = state,
                zipcode = zipcode,
            )
            delivery.save()
            return render(request, 'eshop/shop.html')
        else:
            message = "Il y'a une erreur"
            form = CheckOutForm()
            context = {
                'ms': message,
                'form':form
            }
            return render(request,"eshop/checkout.html", context)
    else:
        form = CheckOutForm()
        context = {
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
            #'order': order,
            'form':form
        }
    return render(request,"eshop/checkout.html", context)
    # try:
    #     customer = Customer.objects.get(user=request.user)
    #     order = Order.objects.get(customer=customer, completed=False)
        
        
    # except ObjectDoesNotExist:
    #     pass
    
    

def login(request):
    return render(request, "eshop/login.html")

def edit_order_item(request, id_product):
    cart = request.session.get('cart', {})
    id_product = str(id_product)

    if request.method == "POST":
        quantity = int(request.POST['qty'])
    else:
        quantity = 1

    if id_product in cart:
        cart[id_product] += quantity
        if cart[id_product] <= 0 :
            del cart[id_product]
    else:
        cart[id_product] = quantity
    request.session['cart'] = cart
    request.session.modified = True
    return redirect(request.META.get('HTTP_REFERER'))
