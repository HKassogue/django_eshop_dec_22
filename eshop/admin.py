from django.contrib import admin
from .models import *
from django.apps import apps
from django.utils.safestring import mark_safe

# Register your models here.
admin.site.register(Image)
# admin.site.register(Category)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'active', 'image_gen', 'products_number']
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ['parent']
    search_fields = ['name', 'id']
    list_filter = ['active', ]
    ordering = ['id', 'name', 'created_at']
    fields = ['name', 'slug', 'active', 'image_gen', 'image', 'products_number']
    readonly_fields = ['image_gen', 'products_number']

    def image_gen(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
                url = obj.image.url,
                width=50,
                height=50,
            )
        )

    def products_number(self, obj):
        return obj.products.count()

class ImageInline(admin.TabularInline):
    model = Image
    fields = ['name', ]
    extra = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'category', 'price', 'stock', 'active']
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ['category']
    search_fields = ['name', 'id']
    ordering = ['id', 'name', 'created_at', 'price', 'stock']
    list_filter = ['active', 'category']
    # fields = ['name', 'slug']
    # exclude = ['price', 'category']
    fieldsets = (
        ("Désignation", {
            # "classes": ["collapse", "start-open"],
            "fields": ("name", "slug", "category", "description")}
        ),
        ("Prix et stock", {
            "description": "msg particulier",
            "fields": ("price", "stock")}
        ),
    )
    inlines = [ImageInline]




# all other models
models = apps.get_models()

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass