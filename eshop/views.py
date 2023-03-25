from datetime import datetime
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .context_processors import *
from .forms import CheckOutForm
from .models import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views here.
def index(request):
    products = Product.objects.filter(active=True).order_by('name')[:12]
    arrivals = Arrival.objects.filter(is_closed=False)
    arrivals_details = []
    for arrival in arrivals:
        arrivals_details += list(Arrival_details.objects.filter(arrival=arrival))
    context = {
        'products': products,
        'arrivals_details': arrivals_details
    }
    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(user=request.user)
            order = Order.objects.filter(customer=customer, completed=False).first()
            if order:
                order_details = Order_details.objects.get(order=order)
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
    filter_Price = Filter_Price.objects.all()
    if cat == 'all':
        if not query:
            if sort == 'latest':
                products = Product.objects.filter(active=True)
            elif sort == 'popular':
                products = Product.objects.filter(active=True).annotate(
                    nbr_likes=Count('likes')).order_by('-nbr_likes')
            else:
                products = Product.objects.filter(active=True).annotate(
                    nbr_reviews=Count('reviews__rate')).order_by('-nbr_reviews')
        else:
            products = Product.objects.filter(name__icontains=query, active=True)
    else:
        if not query:
            if sort == 'latest':
                products = Product.objects.filter(category__slug=cat, active=True)
            elif sort == 'popular':
                products = Product.objects.filter(category__slug=cat, active=True).annotate(
                    nbr_likes=Count('likes')).order_by('-nbr_likes')
            else:
                products = Product.objects.filter(category__slug=cat, active=True).annotate(
                    nbr_reviews=Count('reviews__rate')).order_by('-nbr_reviews')
        else:
            products = Product.objects.filter(category__slug=cat, active=True).filter(name__icontains=query)

    paginator = Paginator(products, perpage)
    try:
        produit = paginator.page(page)
    except PageNotAnInteger:
        produit = paginator.page(1)
    except EmptyPage:
        produit = paginator.page(paginator.num_pages)

    context = {
        'products': produit,
        'filter_Price': filter_Price,
    }
    return render(request, "eshop/shop.html", context)


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
    return render(request, "eshop/shop.html", context)


@csrf_exempt
def check(request):
    if request.method == "GET":
        price = int(request.GET.get('price'))

    product = Product.objects.filter(price__lte=price)
    data = list(product.values())
    for i in range(len(product)):
        data[i]['first_image'] = product[i].first_image

    return JsonResponse(data, safe=False)


def detail(request, id):
    product = Product.objects.get(id=id)
    sim_products = list(Product.objects.filter(category=product.category, active=True).filter(active=True)[:5])
    best_liked = list(Product.objects.filter(active=True).annotate(nbr_likes=Count('likes')).order_by('-nbr_likes'))
    for prod in sim_products:
        if prod in best_liked:
            best_liked.remove(prod)
    sim_products += best_liked[:5]
    best_rated = list(Product.objects.filter(active=True).annotate(nbr_reviews=Count('reviews__rate')).order_by('-nbr_reviews'))
    for prod in sim_products:
        if prod in best_rated:
            best_rated.remove(prod)
    sim_products += best_rated[:5]

    context = {
        'product': product,
        'sim_products': sim_products,
    }
    return render(request, "eshop/detail.html", context)


def contact(request):
    return render(request, "eshop/contact.html", {})


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
    form = CheckOutForm()
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
        context = {
            
            'items': zip(products,quantities),
            'total': total,
            'shipping': shipping,
            'form':form
        }
    return render(request,"eshop/checkout.html", context)


def add_delivery(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        order = Order.objects.get(customer=customer, completed=False)
        context = {
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
            'order': order,
        }
        if request.POST == 'POST':
            order = Order.objects.get(customer=customer, completed=False)
            token = request.POST.get('stripeToken')
            chargeID = stripe_payment(settings.STRIPE_SECRET_KEY,token, order.get_total(),str(order.id))
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
                    price = order.products.price,
                    delivery_by = chargeID,
                    state = state,
                    zipcode = zipcode,
                )
                delivery.save()
                return render(request, 'eshop/shop.html')    
    return render(request, "eshop/cart.html", {'items': zip(products, quantities), 'total': total, 'shipping': shipping, 'coupon': coupon})


def review(request, id):
    if request.method == 'POST':
        product = Product.objects.get(id=id)
        rate = request.POST['rate']
        comment = request.POST['comment']
        name = request.POST['name']
        email = request.POST['email']
        Review(product=product, rate=rate, comment=comment, name=name, email=email).save()
    return redirect('detail', id=id)


def add_to_cart(request):
    cart = request.session.get('cart', {})
    data = json.loads(request.body)
    id_product = data['productId']
    quantity = int(data['quantity'])
    erase = bool(data['erase'])
    
    if id_product in cart and not erase:
        cart[id_product] += quantity
        if cart[id_product] <= 0:
            del cart[id_product]
    else:
        cart[id_product] = quantity
    request.session['cart'] = cart
    request.session.modified = True
    response = {
        "status": "202", 
        "message": "add succefull!",
        "data": f"{id_product} x {quantity}"
    }
    return JsonResponse(response, safe=False)


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


@csrf_exempt
def proceedCheckout(request):
    cart = request.session.get('cart', {})
    order_id = 0
    if cart:
        customer = Customer.objects.get(user=request.user)
        if customer :
            reference = generate_code()
            order = Order(reference=reference,customer=customer)
            if request.method == "GET":
                code_coupon = request.GET.get('code')
                coupon = Coupon.objects.filter(code = code_coupon).filter(validity__gte=datetime.now()).filter(is_valid = True).filter(max_usage__gt=0).first()
                if coupon:
                    order.coupon_id = coupon.id
                    coupon.max_usage = coupon.max_usage - 1
                    coupon.save()

            order.save()
            order_id = order.id
            for id, qty in cart.items():
                id = int(id)
                if id > 0:
                    product = Product.objects.get(id=id)
                    if product.stock > qty:
                        order_detail = Order_details(order=order, product=product, quantity=qty, price=product.price)
                        order_detail.save()
                        product.stock = product.stock - qty
                        product.save()

            del request.session['cart']
            request.session.modified = True
            jsonResponse = {
                "status":"202","message":"update succefull!","data" : order_id
            }
        else:
            jsonResponse = {
                "status":"402","message":"Customer not connect!","data" : order_id
            }
    else:
        jsonResponse = {
            "status":"401","message":"Cart empty!","data" : order_id
        }
    return JsonResponse(jsonResponse)


import secrets
import string


def generate_code():
    alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits
    while True:
        code = ''.join(secrets.choice(alphabet) for i in range(5))
        if not Order.objects.filter(reference=code).exists():
            break
    return code


def like(request):
    data = json.loads(request.body)
    id = data['id']
    product = get_object_or_404(Product, id=int(id))
    likes = request.session.get('likes', {})
    if request.user.is_authenticated:
        email = request.user.email
        # Vérifiez si l'utilisateur a déjà aimé le produit
        like, created = Like.objects.get_or_create(product=product, email=email)
        if not created:
            like.liked = not like.liked
            like.save()
        likes[id] = like.liked
    else:
        email = "anonymoususer@mail.com"
        if id in likes:
            likes[id] = not likes[id]
        else:
            like = Like.objects.create(product=product, email=email)
            likes[id] = like.liked
    request.session['likes'] = likes
    request.session.modified = True
    # return redirect(request.META.get('HTTP_REFERER'))
    data = {
        "status": "202", 
        "message": "like/unlike succefull!",
        "data": id
    }
    return JsonResponse(data, safe=False)


# def filtered_products(request):
#     min_price = request.GET.get('min_price')
#     max_price = request.GET.get('max_price')

#     # filtrer les produits en conséquence
#     products = Product.objects.all()
#     if min_price and max_price:
#         products = products.filter(price=min_price)

#     # passer les produits filtrés au contexte de la vue
#     context = {'products': products}
#     return render(request, 'products.html', context)


def filtered_products(request):
    query = request.GET.get('q', '')
    if not query:
        return redirect('shop')

    page = request.GET.get('page', 1)
    perpage = request.GET.get('per', 6)
    products = Product.objects.filter(price__icontains=query)

    paginator = Paginator(products, perpage)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
    }
    return render(request, "eshop/shop.html", context)
