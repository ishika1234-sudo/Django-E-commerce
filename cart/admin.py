from django.contrib import admin
from .models import Cart, CartItem

# Register your models here.
# class Category_Admin(admin.ModelAdmin):
#     prepopulated_fields = {'slug':('category_name',)}  # so that whenevr we are entering category name is admin panel, slug should automatically take the same name
#     list_display = ('category_name', 'slug', 'date_created') # to display these fields in front page

admin.site.register(Cart)
admin.site.register(CartItem)