from .models import Category

def getCategories(request):
    categories = Category.objects.filter(active=True).order_by('name')
    total = sum([category.products.count() for category in categories])
    return {'categories': categories, 'total': total}

def getDashboardData(request):
    total_ventes = 100000
    total_ventes_week = [1000, 2500, 1800, 4000, 5000, 2000, 1000]
    return {'total_ventes': total_ventes, 'total_ventes_week': total_ventes_week}