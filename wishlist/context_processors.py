from . models import Wishlist_Items, Wishlist
from . import views

def get_count_of_items_in_wishlist(request):
    wishlist_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            if request.user.is_authenticated:
                wishlistitems = Wishlist_Items.objects.all().filter(user=request.user) 
            else:
                wishlist = Wishlist.objects.filter(wishlist_id = views.get_wishlist_id(request))
                wishlistitems = Wishlist_Items.objects.all().filter(wishlist=wishlist[:1]) 
            for items in wishlistitems:
                wishlist_count += 1
        except wishlist.DoesNotExist:
            wishlist_count = 0
    return {'wishlist_count': wishlist_count
           }
