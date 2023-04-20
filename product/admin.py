from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Product, Brand

# Register your models here.
class Product_Admin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('product_name',)}  # so that whenevr we are entering category name is admin panel, slug should automatically take the same name
    list_display = ('product_name', 'price', 'stock','brand', 'is_available','is_new', 'date_modified') # to display these fields in front page

admin.site.register(Product, Product_Admin)

admin.site.register(Brand)