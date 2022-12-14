from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    description = models.TextField(max_length=255, null=True, blank=True)
    price = models.FloatField(null=False, blank=False)
    stock = models.IntegerField(default=1, null=False, blank=False)
    category = models.ForeignKey('Category', null=True, blank=False, on_delete=models.SET_NULL, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)

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
    image = models.ImageField(null=True, blank=True, upload_to='images/categories/')
    parent = models.ForeignKey('Category', null=True, blank=True, 
        related_name='subcategories', on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f" {self.id}: {self.name}"

    @property
    def nbr(self):
        if self.products.all():
            return self.products.count()
        else:
            return 0
    @property
    def subcategories_elts(self):
        return self.products.all()
    