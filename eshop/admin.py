from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from .models import *
from django.apps import apps
from django.utils.safestring import mark_safe

# Register your models here.
# admin.site.register(Image)
# admin.site.register(Category)


@admin.register(Arrival)
class ArrivalsAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'is_closed', 'closed_at', 'products_count']
    search_fields = ['id', 'created_at']
    list_filter = ['is_closed']
    ordering = ['-created_at', 'is_closed', 'id']
    fields = ['id', 'created_at', 'is_closed', 'closed_at']
    readonly_fields = ['id', 'created_at']


@admin.register(Arrival_details)
class ArrivalDetails(admin.ModelAdmin):
    list_display = ['id', 'arrival', 'product', 'quantity']
    autocomplete_fields = ['arrival', 'product']

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


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'avatar_tag', 'address', 'zipcode', 'city']
    search_fields = ['user', 'id']
    readonly_fields = ['avatar']
    autocomplete_fields = ['user']


    

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


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name_tag', 'name', 'product']
    search_fields = ['id', 'name', 'product__name']
    fields = ['name', 'name_tag', 'product']
    autocomplete_fields = ['product']
    readonly_fields = ['name_tag']


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
    autocomplete_fields = ['product']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'rate', 'comment', 'name', 'email', 'product', 'created_at']
    list_filter = ['product']
    autocomplete_fields = ['product']


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'ref', 'payed_at', 'mode', 'details', 'order']
    list_filter = ['mode']
    autocomplete_fields = ['order']


class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            output.append(
                f'<a href="{image_url}" target="_blank">'
                f'<img src="{image_url}" width="50" height="50" '
                f'style="object-fit: cover;"/> </a>')
        output.append(super(AdminFileWidget, self).render(name, value, attrs, renderer))
        return mark_safe(u''.join(output))


class ImageInline(admin.TabularInline):
    model = Image
    # fields = ['name']
    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget}
    }
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price', 'stock', 'active']
    list_display_links = ['id', 'name']
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
            "fields": ("price", "stock")}
        ),
        ("Likes and reviews", {
            "fields": ("likes_total", "reviews_count", "reviews_rate")}
        ),
        ("Solde", {
            "fields": ("orders_count", "solde_amount")}
        ),
    )
    inlines = [ImageInline]
    readonly_fields = ['likes_total', "reviews_count", "reviews_rate", "orders_count", "solde_amount"]




# all other models
models = apps.get_models()

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass