from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    description = models.TextField(max_length=255, null=True, blank=True)
    price = models.DecimalField(null=False, blank=False, decimal_places=2, max_digits=2)
    stock = models.IntegerField(default=1, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    def __str__(self):
        return f"{self.id}: {self.name}"

   
