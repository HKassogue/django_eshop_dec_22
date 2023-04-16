from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from .models import *
from django.apps import apps
from django.utils.safestring import mark_safe
from django.template.defaultfilters import truncatewords


# Register your models here.
# admin.site.register(Image)
# admin.site.register(Category)


class ArrivalProductsInline(admin.TabularInline):
    model = Arrival.products.through
    fields = ['product', 'quantity']
    autocomplete_fields = ['product']
    extra = 0
    #readonly_fields = ['product']
    verbose_name = 'Arrival products details'
    verbose_name_plural = 'Arrivals products details'


@admin.register(Arrival)
class ArrivalsAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'is_closed', 'closed_at', 'products_count']
    search_fields = ['id', 'created_at']
    list_display_links = ['id', 'created_at']
    list_filter = ['is_closed']
    ordering = ['-created_at', 'is_closed', 'id']
    fields = ['id', 'created_at', 'is_closed', 'closed_at']
    readonly_fields = ['id', 'created_at']
    inlines = [ArrivalProductsInline]


@admin.register(Arrival_details)
class ArrivalDetails(admin.ModelAdmin):
    list_display = ['id', 'arrival', 'product', 'quantity']
    search_fields = ['id', 'arrival', 'product']
    autocomplete_fields = ['arrival', 'product']
    list_display_links = ['id', 'arrival']


@admin.register(Alerts)
class Alerts(admin.ModelAdmin):
    list_display = ['id', 'status', 'type', 'details', 'created_at', 'traited_at', 'user']
    list_filter = ['status', 'type']
    search_fields = ['details', 'user', 'id']
    list_display_links = ['id', 'status']
    fields = ['id', 'status', 'type', 'details', 'created_at', 'traited_at', 'user']
    autocomplete_fields = ['user']
    readonly_fields = ['id', 'created_at']
    

@admin.register(Coupon_type)
class CouponType(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    search_fields = ['name', 'id']
    

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'coupon_type', 'description_trunc', 'discount', 'max_usage', 'is_valid', 'created_at']
    search_fields = ['code', 'id']
    list_filter = [ 'coupon_type', 'is_valid']
    list_display_links = ['code']
    ordering = ['-created_at', 'id']
    autocomplete_fields = ['coupon_type']
    readonly_fields = ['id', 'created_at']
    fieldsets = (
        ("References", {
            # "classes": ["collapse", "start-open"],
            "fields": ('id', 'code', )}
        ),
        ("Discount information", {
            # "classes": ["collapse", "start-open"],
            "fields": ('discount', 'coupon_type', 'description')}
        ),
        ("Validity information", {
            "fields": ('max_usage', 'is_valid', 'created_at', 'validity')}
        ),
    )

    def description_trunc(self, obj):
        if len(obj.description) <= 15:
            return obj.description
        return truncatewords(obj.description, 15) + '...'
    description_trunc.short_description = "description"

    def arrival(self, obj): 
        return obj.code


class ProductInline(admin.TabularInline):
    model = Product
    fields = ['name', 'price', 'stock', 'active']
    extra = 0
    sortable_by = ['name', 'price']


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
    inlines = [ProductInline]
    list_display_links = ['id', 'name', 'slug']

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
    list_display = ['id', 'user', 'avatar_tag', 'tel', 'address', 'city', 'zipcode', 'country']
    search_fields = ['user', 'tel', 'id']
    readonly_fields = ['avatar_tag', 'id', 'reviews_count', 'likes_count', 'orders_count']
    autocomplete_fields = ['user']
    list_display_links = ['id', 'user']
    fieldsets = (
        ("User information", {
            # "classes": ["collapse", "start-open"],
            "fields": ('id', 'user', 'avatar', 'avatar_tag')}
        ),
        ("Contacts", {
            # "classes": ["collapse", "start-open"],
            "fields": ('tel', 'address', 'city', 'zipcode', 'country')}
        ),
        ("Interactions", {
            "fields": ('reviews_count', 'likes_count', 'orders_count')}
        ),
    )


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'state', 'address', 'zipcode', 'city', 'country', 'price', 'delivered_at']
    list_filter = ['state']
    search_fields = ['address', 'id', 'order', 'city', 'country']
    autocomplete_fields = ['order', 'delivered_by']
    fieldsets = (
        ("Lieux", {
            # "classes": ["collapse", "start-open"],
            "fields": ('address', 'zipcode', 'city', 'country')}
        ),
        ("Commande et livreur", {
            "fields": ('order', 'state', 'delivered_at', 'delivered_by', 'price')}
        ),
    )
    list_display_links = ['id', 'order']
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'delivered_by':
            kwargs['initial'] = MyUser.objects.get(user=request.user).id
            kwargs['disabled'] = True
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


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
    list_display = ['id', 'product', 'liked', 'email', 'created_at']
    search_fields = ['product', 'email']
    list_filter = ['liked']
    ordering = ['-created_at', '-liked']
    autocomplete_fields = ['product']
    list_per_page = 20


@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'avatar_tag']
    search_fields = ['user', 'id']
    fields = ['user', 'avatar', 'avatar_tag']
    readonly_fields = ['avatar_tag']
    list_display_links = ['id', 'user']
    autocomplete_fields = ['user']


class OrderProductsInline(admin.TabularInline):
    model = Order.products.through
    fields = ['product', 'price', 'quantity']
    autocomplete_fields = ['product']
    extra = 0
    #readonly_fields = ['product']
    verbose_name = 'Order products details'
    verbose_name_plural = 'Order products details'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'reference', 'completed', 'coupon', 'customer', 'subtotal', 'created_at']
    list_display_links = ['id', 'reference']
    list_filter = ['completed']
    search_fields = ['id', 'reference', 'customer', 'coupon']
    autocomplete_fields = ['customer', 'coupon']
    readonly_fields = ['id', 'created_at', 'shipping', 'reduction', 'subtotal', 'total', 'products_count']
    fieldsets = (
        ("Order information", {
            # "classes": ["collapse", "start-open"],
            "fields": ('id', 'reference', 'completed', 'coupon', 'customer', 'created_at')}
        ),
        ("Order amount", {
            "fields": ('shipping', 'reduction', 'subtotal', 'total', 'products_count')}
        ),
    )
    inlines = [OrderProductsInline]


@admin.register(Order_details)
class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity', 'price']
    list_display_links = ['id', 'order']
    search_fields = ['id', 'order', 'product']
    autocomplete_fields = ['order', 'product']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'rate', 'comment_trunc', 'product', 'name', 'email', 'created_at']
    search_fields = ['product', 'comment', 'name', 'email']
    ordering = ['-created_at', '-rate']
    autocomplete_fields = ['product']
    list_per_page = 20
    list_display_links = ['id', 'rate']

    def comment_trunc(self, obj):
        if len(obj.comment) <= 15:
            return obj.comment
        return truncatewords(obj.comment, 15) + '...'
    comment_trunc.short_description = "comment"


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'ref', 'payed_at', 'mode', 'details', 'order']
    list_filter = ['mode']
    list_display_links = ['id', 'ref']
    autocomplete_fields = ['order']
    ordering = ['-payed_at', 'ref']
    fields = ['id', 'ref', 'payed_at', 'mode', 'details', 'order']
    readonly_fields = ['payed_at', 'id']


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