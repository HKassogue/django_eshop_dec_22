from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Category, Order, Order_details, Customer,Coupon
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def index(request):
    products = Product.objects.all()
    context =  {
        'products': products,
    }

    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(user=request.user)
            order = Order_details.objects.get(customer=customer, completed=False)
            if order:
                order_details = Order_details.get(order=order)
                cart = request.session.get('cart', {})
                for item in order_details:
                    key = str(item.product.id)
                    if key in cart:
                        cart[key] += item.quantity
                    else :
                        cart[key] = item.quantity
                    request.session['cart'] = cart
                    request.session.modified = True
                    cart[str(item.product.id)] = item.quantity
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

@csrf_exempt
def product(request):
    #product =  Product.objects.filter(name__icontains="testh")
    product =  Product.objects.all()        
    data=list(product.values())
    for i in range(len(product)):
        data[i]['first_image'] = product[i].first_image
    
    return JsonResponse(data,safe=False)

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
        id = int(id)
        if id > 0:
            product = Product.objects.get(id=id)
            products.append(product)
            quantities.append(qty)
            total += qty * product.price
    return render(request,"eshop/cart.html", {'items': zip(products, quantities), 'total': total, 'shipping': shipping, 'coupon': coupon})

def checkout(request):
    return render(request,"eshop/checkout.html", {})

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

@csrf_exempt
def decreace_increase(request):
    cart = request.session.get('cart', {})
    data = 0
    if request.method == "GET":
        quantity = int(request.GET.get('qty'))
        id_product = int(request.GET.get('id_product')) 
        id_product = str(id_product)

    else:
        quantity = 0

    if id_product in cart:
        cart[id_product] += quantity
        product = Product.objects.get(id=id_product)
        data = quantity * product.price
        if cart[id_product] <= 0 :
            del cart[id_product]

    else:
        cart[id_product] = quantity
    request.session['cart'] = cart
    request.session.modified = True
    return JsonResponse({
        "status":"202","message":"update succefull!","data":data
    })

@csrf_exempt
def del_in_cart(request):
    cart = request.session.get('cart', {})

    if request.method == "GET":
        id_product = int(request.GET.get('id_product')) 
        id_product = str(id_product)

    if id_product in cart:
        if cart[id_product] :
            del cart[id_product]
            request.session['cart'] = cart
            request.session.modified = True
            return JsonResponse({
                "status":"202","message":"update succefull!","data":id_product
            })
    return JsonResponse({
                    "status":"400","message":"error update!"
                })

@csrf_exempt
def coupons(request):
    from datetime import datetime
    if request.method == "GET":
        jsonResponse = {}
        code_coupon = request.GET.get('code')
        coupon = Coupon.objects.filter(code = code_coupon).filter(validity__gte=datetime.now()).filter(is_valid = True).filter(max_usage__gt=0)
        if coupon:
            data=list(coupon.values())
            jsonResponse = {
               "status":"202","message":"update succefull!","data" : data 
            }
        else :
            jsonResponse = {
               "status":"404","message":"Not found!", 
            }
    return JsonResponse(jsonResponse)