from django.contrib import admin
from .models import *
from django.apps import apps
from django.utils.safestring import mark_safe

# Register your models here.
admin.site.register(Product)
admin.site.register(Image)
# admin.site.register(Category)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'active', 'image', 'products_number']
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ['parent']
    search_fields = ['name', 'id']

    def image(self, obj):
        return obj.image.url

    def products_number(self, obj):
        return obj.products.count()

# all other models
models = apps.get_models()

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass