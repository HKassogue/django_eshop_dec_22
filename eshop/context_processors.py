from .models import Category,Order_details,Order, Like, Review 
from datetime import date, datetime


def getCategories(request):
    categories = Category.objects.filter(active=True).order_by('name')
    total = sum([category.products.count() for category in categories])
    return {'categories': categories, 'total': total}

def getDashboardData(request):
    total_ventes = 100000
    total_ventes_week = [1000, 2500, 1800, 4000, 5000, 2000, 1000]
    return {'total_ventes': total_ventes, 'total_ventes_week': total_ventes_week}

def getCountOrderByDay(request):
   current_date=datetime.now()
   order=Order.objects.filter(created_at__date = date.today())
   nombre = order.count()
#    order_details=order.order_details()
#    somme = 0
#    for order in order_details:
#        somme += order.quantity * order.product.price
   return  {"nombre":nombre}

def getCountOrderByMonth(request):
   current_date=datetime.now()
   order=Order.objects.filter(created_at__month = date.today().month)
   month = order.count()
   return  {"month":month}

def getCountLike(request):
   like = Like.objects.count()
   return  {"like":like}

def getCountReview(request):
   review = Review.objects.count()
   return  {"review":review}

