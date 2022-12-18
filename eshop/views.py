from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.http import JsonResponse
import json

# Create your views here.
def index(request):
    products = Product.objects.all()
    customer = request.user
    order, created = Order.objects.get_or_create(customer=customer, completed=False)
    items = order.products.all()
    return render(request, "eshop/index.html", {'products': products, 'order': order, 'items': items})

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

def update_item(request):
    #return JsonResponse('Item was added', safe=False)
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']

    customer = request.user
    product = Product.objects.get(id=productID)
    order, created = Order.objects.get_or_create(customer=customer, completed=False)

    item, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        item.quantity += 1
    elif action == 'remove':
        item.quantity -= 1
    item.save()
    if item.quantity <= 0:
        item.delete()