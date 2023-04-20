from django.contrib import admin

from .models import Wishlist, Wishlist_Items


admin.site.register(Wishlist)
admin.site.register(Wishlist_Items)