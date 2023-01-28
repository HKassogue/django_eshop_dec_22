from django.db import models
from django.contrib.auth.models import User

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


class Image(models.Model):
    name = models.ImageField(null=True, blank=True, upload_to='images/products/')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f"{self.id}: {self.name}"


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
        return f" {self.id}: {self.name}"


class MyUser(models.Model):
    user = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='images/users/', null=True, blank=True)
    

class Customer(models.Model):
    user = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='images/customers/', null=True, blank=True)
    address = models.CharField(max_length=30, null=True, blank=True)
    zipcode = models.CharField(max_length=6, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)


class Review(models.Model):
    rate = models.FloatField(null=False, blank=False)
    comment = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=30, null=False, blank=False)
    email = models.CharField(max_length=30, null=False, blank=False)
    product = models.ForeignKey('Product', null=False, blank=False, 
        on_delete=models.CASCADE, related_name='reviews')
    created_at = models.DateTimeField(null=False, blank=False, auto_now=True)

class Like(models.Model):
    email = models.CharField(max_length=30, null=False, blank=False)
    liked = models.BooleanField(default=True, null=False, blank=False)
    product = models.ForeignKey('Product', null=False, blank=False, 
        on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(null=False, blank=False, auto_now=True)


class Coupon_type(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False, unique=True)

class Coupon(models.Model):
    code = models.CharField(max_length=30, null=False, blank=False, unique=True)
    description = models.TextField(null=True, blank=True)
    coupon_type = models.ForeignKey('Coupon_type', null=True, blank=True, on_delete=models.SET_NULL)
    discount = models.SmallIntegerField(default=1, null=True, blank=False)
    max_usage = models.SmallIntegerField(default=1, null=True, blank=False)
    validity = models.DateTimeField(null=False, blank=False)
    is_valid = models.BooleanField(default=True, null=False, blank=False)
    created_at = models.DateTimeField(null=False, blank=False, auto_now=True)

