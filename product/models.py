from django.db import models

# Create your models here.
from django.db import models
from category.models import Category
from django.urls import reverse

class Brand(models.Model):
    brand_name = models.CharField(max_length=250, unique=True)
    date_created = models.DateTimeField(auto_now_add =True)

    def __str__(self):
        return self.brand_name


# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    product_description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    product_image = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    is_new = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE ) # on deleting the category, the products associated to them will also delete
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE) 
    date_created = models.DateTimeField(auto_now_add =True)
    date_modified = models.DateTimeField(auto_now =True)

    def get_url(self):
        return reverse('product_details', args=[self.category.slug, self.slug])
    
    def __str__(self) -> str:
        return self.product_name
    
# variation_category_choice = (
#     ('color', 'color'),
#     ('size', 'size'),
# )

# class VariationManager(models.Manager):
#     def colors(self):
#         return super(VariationManager, self).filter(variation_category='color', is_active=True)

#     def size(self):
#         return super(VariationManager, self).filter(variation_category='size', is_active=True)
    
# class Variation(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     variation_category = models.CharField(max_length=100, choices=variation_category_choice)
#     variation_value = models.CharField(max_length=100)
#     is_active = models.BooleanField(default=True)
#     date_created = models.DateTimeField(auto_now=True)

#     # tell the model that there is a manager created for it
#     object = VariationManager()

#     def __str__(self):
#         return self.variation_value