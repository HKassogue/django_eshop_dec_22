from datetime import datetime
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Arrival, Arrival_details, Like, Product, Order, Order_details, Customer
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST



# Create your views here.
def index(request):
    products = Product.objects.all()
    
    current_time = datetime.now()
    upcoming_arrivals = Arrival.objects.filter(closed_at__gt=current_time, is_closed=False)
    produits = []
    for arrival in upcoming_arrivals:
        arrival_details = arrival.arrival_details_set.all()
        for detail in arrival_details:
            product = detail.product
            quanti = detail.quantity
            image = product.first_image
            price = product.price
            day = arrival.closed_at
            nam = product.name
            produits.append((product, quanti, image, price,nam,day))
    context =  { 'produits': produits,
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

def like_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    email = request.POST.get('email') # récupérer l'adresse e-mail de l'utilisateur connecté ou d'un cookie
    liked = request.POST.get('liked', 'true') == 'true'
    Like.objects.update_or_create(email=email, product=product, defaults={'liked': liked})
    like_count = product.likes.filter(liked=True).count()
    return JsonResponse({'liked': liked, 'like_count': like_count})

def like(request):
    if request.method == 'POST':
        product_id = request.POST.get('product.id')
        email = request.POST.get('email')
        
        # Vérifiez si l'utilisateur a déjà aimé le produit
        like, created = Like.objects.get_or_create(product_id=product_id, email=email)
        
        if not created:
            like.liked = not like.liked
            like.save()
            
        # Mettre à jour le nombre de likes dans le modèle de produit
        product = Like.objects.get(id=product_id)
        product.likes = product.likes_count()
        product.save()
        
        # Retourner une réponse JSON avec le nombre de likes mis à jour
        data = {'likes': product.likes}
        return JsonResponse(data)
@require_POST
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = request.session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + 1
    request.session['cart'] = cart
    return redirect('cart')

