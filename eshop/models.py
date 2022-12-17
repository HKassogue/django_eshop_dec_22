from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    description = models.TextField(max_length=255, null=True, blank=True)
    price = models.FloatField(null=False, blank=False)
    stock = models.IntegerField(default=1, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    def __str__(self):
        return f"{self.id}: {self.name}"

class Image(models.Model):
    name = models.ImageField(null=True, blank=True, upload_to='products/images/')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f"{self.id}: {self.name}"


