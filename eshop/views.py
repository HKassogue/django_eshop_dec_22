from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Category, Order, Order_details, Customer, Filter_Price
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def index(request):
    products = Product.objects.all()
    context = {
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
# filter_price get
    filter_Price = Filter_Price.objects.all()

    if cat == 'all':
        if not query:
            if sort == 'latest':
                products = Product.objects.all()
            elif sort == 'popular':
                products = Product.objects.all().annotate(
                    nbr_likes=Count('likes')).order_by('-nbr_likes')
            else:
                products = Product.objects.all().annotate(
                    nbr_reviews=Count('reviews__rate')).order_by('-nbr_reviews')
        else:
            products = Product.objects.filter(name__icontains=query)
    else:
        if not query:
            if sort == 'latest':
                products = Product.objects.filter(category__slug=cat)
            elif sort == 'popular':
                products = Product.objects.filter(category__slug=cat).annotate(
                    nbr_likes=Count('likes')).order_by('-nbr_likes')
            else:
                products = Product.objects.filter(category__slug=cat).annotate(
                    nbr_reviews=Count('reviews__rate')).order_by('-nbr_reviews')

        else:
            products = Product.objects.filter(
                category__slug=cat).filter(name__icontains=query)

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
        'products': products,
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
    sim_products = Product.objects.filter(
        category=product.category).filter(active=True)

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
        product = Product.objects.get(id=int(id))
        products.append(product)
        quantities.append(qty)
        total += qty * product.price
    return render(request, "eshop/cart.html", {'items': zip(products, quantities), 'total': total, 'shipping': shipping, 'coupon': coupon})


def checkout(request):
    return render(request, "eshop/checkout.html", {})


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
        if cart[id_product] <= 0:
            del cart[id_product]
    else:
        cart[id_product] = quantity
    request.session['cart'] = cart
    request.session.modified = True
    return redirect(request.META.get('HTTP_REFERER'))


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
