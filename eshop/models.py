import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.safestring import mark_safe
from django_countries.fields import CountryField

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    slug = models.CharField(max_length=35, null=True, blank=True, 
        unique=True)
    description = models.TextField(max_length=255, null=True, blank=True)
    price = models.FloatField(null=False, blank=False)
    stock = models.IntegerField(default=1, null=False, blank=False)
    category = models.ForeignKey('Category', null=True, blank=False, on_delete=models.SET_NULL, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    active = models.BooleanField(default=True, null=False, blank=False)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.id}: {self.name}"

    @property
    def first_image(self):
        if self.images.all():
            return self.images.all()[0].name.url
        else:
            return ''

    @property
    def fake_promo(self):
        return self.price * 1.09

    @property
    def reviews_rate(self):
        if not self.reviews.all():
            return 0
        from django.db.models import Avg
        return self.reviews.all().aggregate(mean=Avg('rate'))['mean']

    @property
    def likes_total(self):
        return self.likes.filter(liked=True).count()

class Image(models.Model):
    name = models.ImageField(null=True, blank=True, upload_to='images/products/')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')

    def name_tag(self):
        return mark_safe('<img src="/media/{url}" width="{width}" height={height} />'.format(
                url = self.avatar.name,
                width=50,
                height=50,
            )
        ) 

    def __str__(self):
        return f"{self.name}"


class Category(models.Model):
    name = models.CharField(max_length=45, null=False, blank=False, unique=True)
    slug = models.CharField(max_length=35, null=True, blank=True, 
        unique=True)
    active = models.BooleanField(default=True, null=False, blank=False)
    created_at = models.DateTimeField(null=False, blank=False, 
        auto_now=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/categories/')
    parent = models.ForeignKey('Category', null=True, blank=True, 
        related_name='subcategories', on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.name}"


class MyUser(models.Model):
    user = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='images/users/', null=True, blank=True)
    
    def avatar_tag(self):
        return mark_safe('<img src="/media/{url}" width="{width}" height={height} />'.format(
                url = self.avatar.name,
                width=50,
                height=50,
            )
        ) 
    def __str__(self):
        return f"{self.user.username}"


class Customer(models.Model):
    user = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='images/customers/', null=True, blank=True)
    address = models.CharField(max_length=30, null=True, blank=True)
    zipcode = models.CharField(max_length=6, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)

    def avatar_tag(self):
        return mark_safe('<img src="/media/{url}" width="{width}" height={height} />'.format(
                url = self.avatar.name,
                width=50,
                height=50,
            )
        ) 
    def __str__(self):
        return f"{self.user.username}"


class Review(models.Model):
    rate = models.FloatField(null=False, blank=False, default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=30, null=False, blank=False)
    email = models.CharField(max_length=30, null=False, blank=False)
    product = models.ForeignKey('Product', null=False, blank=False, 
        on_delete=models.CASCADE, related_name='reviews')
    created_at = models.DateTimeField(null=False, blank=False, auto_now=True)

    @property
    def user_photo(self):
        customer = Customer.objects.get(user__email=self.email)
        if customer and customer.avatar:
            return customer.avatar.url
        return ''

class Like(models.Model):
    email = models.CharField(max_length=30, null=False, blank=False)
    liked = models.BooleanField(default=True, null=False, blank=False)
    product = models.ForeignKey('Product', null=False, blank=False, 
        on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(null=False, blank=False, auto_now=True)
    def __str__(self):
        return f"{self.id}"



class Coupon_type(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False, unique=True)
    def __str__(self):
        return f"{self.name}"


class Coupon(models.Model):
    code = models.CharField(max_length=30, null=False, blank=False, unique=True)
    description = models.TextField(null=True, blank=True)
    coupon_type = models.ForeignKey('Coupon_type', null=True, blank=True, on_delete=models.SET_NULL)
    discount = models.SmallIntegerField(default=1, null=True, blank=False)
    max_usage = models.SmallIntegerField(default=1, null=True, blank=False)
    validity = models.DateTimeField(null=False, blank=False)
    is_valid = models.BooleanField(default=True, null=False, blank=False)
    created_at = models.DateTimeField(null=False, blank=False, auto_now=True)
    def __str__(self):
        return f"{self.code}"



class Order(models.Model):
    reference = models.CharField(max_length=30, null=False, blank=False, unique=True)
    coupon = models.ForeignKey('Coupon', null=True, blank=True, on_delete=models.SET_NULL, 
        related_name='orders')
    customer = models.ForeignKey('Customer', null=True, blank=False, 
        on_delete=models.SET_NULL, related_name='orders')
    created_at = models.DateTimeField(null=False, blank=False, auto_now=True)
    products = models.ManyToManyField('Product', through='Order_details', related_name='orders')
    completed = models.BooleanField(default=False, null=True, blank=False)
    
    def get_total (self):
        total = 0
        for order_item in self.products.all():
            total += order_item.get_total_price()
        return total
    @property
    def order_details(self):
       if self.Order_details.all():
           return self.Order_details.all()

    def __str__(self):
        return f"{self.id}: {self.reference}"


class Order_details(models.Model):
    order = models.ForeignKey('Order', null=True, blank=False, on_delete=models.SET_NULL)
    product = models.ForeignKey('Product', null=True, blank=False, on_delete=models.SET_NULL)
    quantity = models.SmallIntegerField(default=1, null=True, blank=False)
    price = models.SmallIntegerField(default=1, null=True, blank=False)
    
    def __str__(self):
        return f"{self.id}"
    
    def get_total_price (self):
        return self.quantity * self.price



class Arrival(models.Model):
    created_at = models.DateTimeField(null=False, blank=False, auto_now=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    is_closed = models.BooleanField(default=False, null=False, blank=False)
    products = models.ManyToManyField('Product', through='Arrival_details', related_name='+')
    def __str__(self):
        return f"{self.id} on {self.created_at}"
    
class Arrival_details(models.Model):
    arrival = models.ForeignKey('Arrival', null=True, blank=False, on_delete=models.SET_NULL)
    product = models.ForeignKey('Product', null=True, blank=False, on_delete=models.SET_NULL)
    quantity = models.SmallIntegerField(default=1, null=True, blank=True)
    def __str__(self):
        return f"{self.arrival.id} : {self.product.name} x {self.quantity}"

class Delivery(models.Model):
    address = models.CharField(max_length=30, null=False, blank=False)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    country = CountryField(multiple=False, blank=True, null=True)
    zipcode = models.CharField(max_length=30, null=False, blank=False)
    city = models.CharField(max_length=30, null=False, blank=False)
    price = models.FloatField(default=0, null=False, blank=False)
    state = models.CharField(max_length=30, null=True, blank=True)
    order = models.ForeignKey('Order', null=False, blank=False, on_delete=models.PROTECT, 
        related_name='deliveries')
    delivered_by = models.ForeignKey('MyUser', null=True, blank=True, on_delete=models.SET_NULL, 
        related_name='+')
    def __str__(self):
        return f"{self.id}"

class Payments(models.Model):
    ref = models.CharField(max_length=30, null=False, blank=False, unique=True)
    payed_at = models.DateTimeField(null=False, blank=False, auto_now=True)
    mode = models.CharField(max_length=30, default='Liquidity', null=False, blank=False)
    details = models.TextField(null=True, blank=True)
    order = models.OneToOneField('Order', on_delete=models.PROTECT, related_name='payment')

    def __str__(self):
        return f"{self.ref}"



class Alerts(models.Model):
    status = models.CharField(max_length=30, null=False, blank=False)
    type = models.CharField(max_length=30, null=False, blank=False)
    details = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(null=False, blank=False, auto_now=True)
    traited_at = models.DateTimeField(null=False, blank=False)
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.PROTECT, 
        related_name='+')
    
    def __str__(self):
        return f"{self.id}"


class Faqs(models.Model):
    type = models.CharField(max_length=30, null=False, blank=False)
    question = models.TextField(null=True, blank=True)
    answer = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(null=False, blank=False, auto_now=True)

    def __str__(self):
        return f"{self.question}"

class Filter_Price(models.Model):
    price = models.CharField(max_length=50, choices=[('0 - 1000', '0 - 1000'), ('1000 - 2000', '1000 - 2000'), ('2000 - 3000', '2000 - 3000'), ('3000 - 4000', '3000 - 4000'), ('4000 - 5000', '4000 - 5000'), ('5000 - 10000', '5000 - 10000')])