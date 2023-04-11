from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .context_processors import *
from .forms import CheckOutForm
from .models import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
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
            order = Order.objects.get(customer=customer, completed=False)
            if order:
                order_details = Order_details.objects.filter(order=order)
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
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            pass
    return render(request, "eshop/index.html", context)


def shop(request, cat='all'):
    page = request.GET.get('page', 1)
    perpage = request.GET.get('per', 6)
    sort = request.GET.get('sort', 'latest')
    query = request.GET.get('q', '')
    price_brackets = Filter_Price.objects.all()
    if request.method == 'POST':
        price_bracket = request.POST['price']
        price_min = request.POST['price_min']
        price_max = request.POST['price_max']
        if price_bracket != 'all':
            price_bracket = Filter_Price.objects.get(id=int(price_bracket))
            price_min = price_bracket.min
            price_max = price_bracket.max
        elif price_min and price_max:
            price_min = float(price_min)
            price_max = float(price_max)
        elif price_min:
            price_min = float(price_min)
            price_max = 'inf'
        elif price_max:
            price_min = 0
            price_max= float(price_max)
        else:
            price_min = 0
            price_max = 'inf'
    else:
        price_min = 0
        price_max = 'inf'
    
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

    products = list(products)
    if price_min > 0:
        products = [product for product in products if product.price >= price_min]
    if price_max != 'inf':
        products = [product for product in products if product.price <= price_max]
    
    paginator = Paginator(products, perpage)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
        'price_brackets': price_brackets,
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
    coupon = None
    for id, qty in cart.items():
        id = int(id)
        if id > 0:
            product = Product.objects.get(id=id)
            products.append(product)
            quantities.append(qty)
            total += qty * product.price
    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(user=request.user)
            order = Order.objects.get(customer=customer, completed=False)
            if order and order.coupon:
                coupon = order.coupon
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            pass
    return render(request,"eshop/cart.html", {'items': zip(products, quantities), 'total': total, 'shipping': shipping, 'coupon': coupon})


@login_required(login_url='login')
def checkout(request):
    form = CheckOutForm()
    try:
        customer = Customer.objects.get(user=request.user)
        order = Order.objects.get(customer=customer, completed=False)
        items = Order_details.objects.filter(order=order)
        context = {
            'order': order,
            'items': items,
            'customer': customer,
            'form':form
        }
        return render(request,"eshop/checkout.html", context)
    except (ObjectDoesNotExist, MultipleObjectsReturned):
        # redirect(request.META.get('HTTP_REFERER', '/'))
        redirect('cart')


@login_required(login_url='login')
def add_delivery(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        form = CheckOutForm(request.POST)
        if form.is_valid():
            # getting form data
            email = form.cleaned_data.get('email')
            mobile = form.cleaned_data.get('mobile')
            address = form.cleaned_data.get('address')
            city = form.cleaned_data.get('city')
            country = form.cleaned_data.get('country')
            zipcode = form.cleaned_data.get('zipcode')
            payment_option = form.cleaned_data.get('payment_option')
            # adding delivery info
            Delivery.objects.create(
                order=order,
                mobile = mobile,
                address = address,
                city = city,
                country = country,
                zipcode = zipcode,
                price = order.shipping,
                state = 'Undelivered',
            )
            # proceeding to payment by Stripe API
            token = request.POST.get('stripeToken')
            chargeID = stripe_payment(settings.STRIPE_SECRET_KEY, token, order.get_total, str(order.id))
            # if payment success
            if chargeID:
                # adding payment info
                Payments.objects.create(
                    ref=generate_ref(),
                    mode=payment_option,
                    detail=str(chargeID),
                    order=order
                )
                # updating products stock and completing order
                for item in Order_details.objects.filter(order=order):
                    item.product.stock -= item.quantity
                    item.product.save()
                order.completed = True
                order.save()
                # send an email
            else:
                # display failure information
                pass
    return redirect('checkout')


def review(request):
    data = json.loads(request.body)
    product = Product.objects.get(id=int(data['productId']))
    rate = data['rate']
    comment = data['comment']
    name = data['name']
    email = data['email']
    Review(product=product, rate=rate, comment=comment, name=name, email=email).save()
    # return redirect('detail', id=id)
    # return redirect(request.META.get('HTTP_REFERER', '/'))
    response = {
        "status": "202", 
        "message": "review succefull!",
        "data": f"{product.id} => {rate}"
    }
    return JsonResponse(response, safe=False)


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
        coupon = Coupon.objects.filter(code=code_coupon).filter(validity__gte=timezone.now()).filter(is_valid = True).filter(max_usage__gt=0)
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
    if cart:
        if request.user.is_authenticated:
            try:
                customer = Customer.objects.get(user=request.user)
                order, created = Order.objects.get_or_create(customer=customer, completed=False)
                if created:
                    order.reference = generate_code()
                if request.method == "GET":
                    code_coupon = request.GET.get('code')
                    coupon = Coupon.objects.filter(code=code_coupon, validity__gte=timezone.now(), is_valid=True, max_usage__gt=0).first()
                    if coupon:
                        order.coupon = coupon
                        coupon.max_usage -= 1
                        coupon.save()
                order.save()
                for id, qty in cart.items():
                    id = int(id)
                    if id > 0:
                        product = Product.objects.get(id=id)
                        if product.stock == 0:
                            if Order_details.objects.filter(order=order, product=product).exists():
                                Order_details.objects.filter(order=order, product=product).delete()
                            continue
                        else:
                            if product.stock < qty:
                                qty = product.stock  # on attribuera le stock disponible si rupture de stock
                            # product.stock = product.stock - qty  # on réduira le stock que lorsque la commande sera payée.
                            # product.save()
                            Order_details.objects.update_or_create(order=order, product=product, defaults={'quantity': qty, 'price': product.price})
                request.session['cart'] = {}
                request.session.modified = True
                jsonResponse = {
                    "status": "202", "message": "update succefull!", "data": order.id
                }
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                jsonResponse = {
                    "status": "402", "message": "Customer most be connected!", "data": 0
                }
        else:
            jsonResponse = {
                "status": "402", "message": "Customer not connected!", "data": 0
            }
    else:
        jsonResponse = {
            "status": "401", "message": "Cart empty!", "data": 0
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


def generate_ref():
    alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits
    while True:
        code = ''.join(secrets.choice(alphabet) for i in range(5))
        if not Payments.objects.filter(ref=code).exists():
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
