from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, "eshop/index.html", {})

def shop(request):
    return render(request, "eshop/shop.html", {})