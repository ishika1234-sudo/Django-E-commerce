from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from . models import Wishlist, Wishlist_Items
from product.models import Product
from django.http import HttpResponse

# Create your views here.
def get_wishlist_id(request): # gets the wishlist session
    wishlist = request.session.session_key
    if not wishlist:
        wishlist = request.session.create()
    return wishlist  

def add_wishlist(request, product_id):
    # wishlist = ''
    # wishlist_item = ''
    product = Product.objects.get(id=product_id) # fetch the product
    try:
        wishlist = Wishlist.objects.get(wishlist_id=get_wishlist_id(request))
    except Wishlist.DoesNotExist:
        wishlist = Wishlist.objects.create(
            wishlist_id = get_wishlist_id(request)
        )
    wishlist.save()
    if request.user.is_authenticated:
        try:
            wishlist_item = Wishlist_Items.objects.get(product=product, wishlist = wishlist) # fetches the wishlist item      
            wishlist_item.quantity += 1
            wishlist_item.save()
        except Wishlist_Items.DoesNotExist:
            wishlist_item = Wishlist_Items.objects.create(
                product = product, 
                quantity = 1, 
                wishlist = wishlist,
                user = request.user
            )
            wishlist_item.save()
    else:
        try:
            wishlist_item = Wishlist_Items.objects.get(product=product, wishlist = wishlist) # fetches the wishlist item
            wishlist_item.quantity += 1
            wishlist_item.save()
        except Wishlist_Items.DoesNotExist:
            wishlist_item = Wishlist_Items.objects.create(
                product = product, 
                quantity = 1, 
                wishlist = wishlist,
            )
            wishlist_item.save()
    return redirect('wishlist')

def remove_from_wishlist(request, product_id):
    
    try:
        wishlist = Wishlist.objects.get(wishlist_id = get_wishlist_id(request))
        product = get_object_or_404(Product, id=product_id)
        wishlist_item = Wishlist_Items.objects.get(product=product, wishlist=wishlist)
        wishlist_item.delete()
        return redirect('wishlist')   
    except Exception as e:
        raise e

def wishlist(request, quantity=0):
    wishlistItems = ''
    try:
        if request.user.is_authenticated:
            wishlistItems = Wishlist_Items.objects.filter(user=request.user)
        else:
            wishlist = Wishlist.objects.get(wishlist_id = get_wishlist_id(request))
            wishlistItems = Wishlist_Items.objects.filter(wishlist=wishlist, is_active=True)
        for wishlistItem in wishlistItems:
            quantity += wishlistItem.quantity
    except ObjectDoesNotExist:
        pass

    data = {
        'quantity': quantity,
        'wishlistItems': wishlistItems
    }
    return render(request,'wishlist.html', data)