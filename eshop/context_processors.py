from .models import Category, Order

def getCategories(request):
    categories = Category.objects.filter(active=True).order_by('name')
    total = sum([category.products.count() for category in categories])
    return {'categories': categories, 'total': total}

def getDashboardData(request):
    # orders = Order.objects.filter(completed=True, created_at__week__lte=1)
    week_solde = 100000
    week_soldes = [500, 2500, 4000, 2000, 1000, 8000, 500]
    return {'week_solde': week_solde, 'week_soldes': week_soldes}