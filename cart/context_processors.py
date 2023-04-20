from . models import Cart, CartItem
from . import views

def get_count_of_items_in_cart(request):
    cart_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id = views.get_cart_id(request))
            cartitems = CartItem.objects.all().filter(cart=cart[:1]) 
            for cartitem in cartitems:
                cart_count += 1
        except cart.DoesNotExist:
            cart_count = 0
    return {'cart_count': cart_count
           }
