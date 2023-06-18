from django.contrib import admin
from .models import Cart, CartItem

# Register your models here.
# class Category_Admin(admin.ModelAdmin):
#     prepopulated_fields = {'slug':('category_name',)}  # so that whenevr we are entering category name is admin panel, slug should automatically take the same name
#     list_display = ('category_name', 'slug', 'date_created') # to display these fields in front page

class cartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'date_added')

class cartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'is_active')

admin.site.register(Cart, cartAdmin)
admin.site.register(CartItem, cartItemAdmin)