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

    @property
    def first_image(self):
        if self.images.all():
            return self.images.all()[0].name.url
        else:
            return ''


class Image(models.Model):
    name = models.ImageField(null=True, blank=True, upload_to='products/images/')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f"{self.id}: {self.name}"


class Order(models.Model):
    reference = models.CharField(max_length=64, null=False, blank=False)
    #costumer = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)
    products = models.ManyToManyField('Product', through='OrderItem', related_name="orders")

    def __str__(self):
        return f'{self.reference}'

    # def save(self, *args, **kwargs) :
    #     super().save(*args, **kwargs)
    #     self.total = 0
    #     for elt in Vente_piece.objects.filter(vente__id=self.id):
    #         self.total += elt.pv_unitaire * elt.quantite
    #         elt.piece.q_stock -= elt.quantite
    #         elt.piece.save()
    #         if elt.piece.q_stock<elt.piece.q_cmd:
    #             cmd, _etat = Commande.objects.get_or_create(statut = "Edition")
    #             cmd.pieces.add(piece = elt.piece, quantite = elt.piece.q_cmd)
    #             cmd.save()
    #     self.num = str(self.id).zfill(4) + '-' + str(datetime.datetime.today().year)
    #     super().save(*args, **kwargs)


class OrderItem(models.Model):
    product = models.ForeignKey('Product', null=True, on_delete=models.SET_NULL)
    order = models.ForeignKey('Order', null=True, on_delete=models.SET_NULL)
    quantity = models.PositiveSmallIntegerField(default=1)
    price = models.FloatField(null=True)