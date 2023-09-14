from django.db import models
from product.models import Product
from django.conf import settings

# Create your models here.
class Wishlist(models.Model):
    wishlist_id = models.CharField(max_length=250)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.wishlist_id
    
class Wishlist_Items(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.wishlist)
