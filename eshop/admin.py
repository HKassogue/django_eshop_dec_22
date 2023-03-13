from django.contrib import admin
from .models import *
from django.apps import apps
from django.utils.safestring import mark_safe

# Register your models here.
admin.site.register(Image)
# admin.site.register(Category)

@admin.register(Arrival)
class ArrivalsAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_closed', 'closed_at', 'products']
    def products(self, obj):
        return obj.len()

@admin.register(Arrival_details)
class ArrivalDetails(admin.ModelAdmin):
    list_display = ['id', 'arrival', 'product', 'quantity']
    def products(self, obj):
        return obj.len()

@admin.register(Alerts)
class Alerts(admin.ModelAdmin):
    list_display = ['id', 'status', 'type', 'details', 'created_at', 'traited_at', 'user']
    def arrival(self, obj):
        return obj.len()

@admin.register(Coupon_type)
class CouponType(admin.ModelAdmin):
    list_display = ['id', 'name']
    def coupon_type(self, obj):
        return obj.name

@admin.register(Coupon)
class Coupon(admin.ModelAdmin):
    list_display = ['id', 'code','coupon_type', 'description', 'discount', 'max_usage', 'validity', 'is_valid', 'created_at']
    search_fields = ['code', 'id']
    list_filter = [ 'coupon_type', 'is_valid']
    #autocomplete_fields = ['coupon_type']

    def arrival(self, obj): 
        return obj.code


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'active', 'image_gen', 'products_number']
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ['parent']
    search_fields = ['name', 'id']
    list_filter = ['active']
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
    fields = ['name', 'name_tag']
    extra = 0
 

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'avatar_tag', 'address', 'zipcode', 'city']
    search_fields = ['user', 'id']
    readonly_fields = ['avatar']

    

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['id', 'address', 'zipcode', 'city', 'price', 'order', 'delivered_by']
    search_fields = ['address', 'id', 'order']
    autocomplete_fields = ['order']
    fieldsets = (
        ("Lieux", {
            # "classes": ["collapse", "start-open"],
            "fields": ('address', 'zipcode', 'city')}
        ),
        ("Commande et livreur", {
            "fields": ('order', 'delivered_by', 'price')}
        ),
    )

#@admin.register(Faqs)
class FaqsAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'question', 'answer']
    search_fields = ['id', 'question']

#@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'product']
    search_fields = ['id', 'name']
    def name(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
                url = obj.name.url,
                width=50,
                height=50,
            )
        ) 


@admin.register(Faqs)
class FaqsAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'question', 'answer']
    search_fields = ['id', 'question']

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'product']

@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'avatar_tag']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'reference', 'coupon', 'customer', 'created_at', 'completed']
    search_fields = ['id', 'reference']
    autocomplete_fields = ['customer', 'coupon']
    #fields = ['reference', 'completed', 'coupon', 'customer']



@admin.register(Order_details)
class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity', 'price']
    search_fields = ['id', 'order']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'rate', 'comment', 'name', 'email', 'product', 'created_at']
    list_filter = ['product']



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