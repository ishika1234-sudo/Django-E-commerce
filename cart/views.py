from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from . models import Cart, CartItem
from product.models import Product, Variation

# Create your views here.
def get_cart_id(request): # private method
    cart = request.session.session_key
    # if there is no session then create a new one
    if not cart:
        cart = request.session.create()
    return cart  # returns the cart id

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id) # fetch the product
    product_variation = []
    if request.method == 'POST':
        
        for item in request.POST:
            key = item
            value = request.POST.get(key)
            print(key +":"+value)

            try:
                variation = Variation.object.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                
                product_variation.append(variation) # get list of variations
                print('product_variation',product_variation)
            except Exception as e:
                print('exception', e)

    try:
        cart = Cart.objects.get(cart_id=get_cart_id(request))  # get the cart_id present in session, and match cart_id with session_id
        print('CART:',cart, 'SESSION:', get_cart_id)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = get_cart_id(request)
        )
    cart.save()
    is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product,cart=cart) # return the cart item objects
        #check what all variations are present in that cart item

        # if the current variation is inside the existing variation increase the qty
        ex_variation_list = []
        cart_item_ids = []
        for item in cart_item:
            existing_variation = item.variation.all()
            ex_variation_list.append(list(existing_variation))
            cart_item_ids.append(item.id)
        print('ex variations:',ex_variation_list)

        if product_variation in ex_variation_list:
            # increase the qty of cart item
            index = ex_variation_list.index(product_variation)
            cart_item_id = cart_item_ids[index]
            item = CartItem.objects.get(product=product, id=cart_item_id)
            item.quantity += 1
            item.save()
        else:
            # create new cart item
            item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if len(product_variation) > 0:
                item.variation.clear()
                item.variation.add(*product_variation)
            item.save()
    # when cart item doesnt exist, create new
    else:
        cart_item = CartItem.objects.create(
            product = product, 
            quantity = 1, 
            cart = cart,
        )
        if len(product_variation) > 0:
            cart_item.variation.clear()
            cart_item.variation.add(*product_variation)
        cart_item.save()
    # return HttpResponse(cart_item.product)
    # exit()
    #return user to cart page
    return redirect('cart')

def remove_from_cart(request, product_id, cart_item_id):
    try:
        cart = Cart.objects.get(cart_id = get_cart_id(request))
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.get(product=product, cart=cart,id=cart_item_id)
        cart_item.delete()
        return redirect('cart')   
    except Exception as e:
        raise e


def decrement_cart_item(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id = get_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:    
            cart_item.delete()
    except:
        pass
    return redirect('cart')   

def cart(request, total=0, quantity=0, tax=0, grandTotal=0):
    try:
        cartItems = ''
        cart = Cart.objects.get(cart_id = get_cart_id(request))
        cartItems = CartItem.objects.filter(cart=cart, is_active=True)
        for cartItem in cartItems:
            total += cartItem.product.price * cartItem.quantity
            quantity += cartItem.quantity
        tax = (3 * total) / 100
        grandTotal = total + tax
    except ObjectDoesNotExist:
        pass
    data = {
        'total': total,
        'quantity': quantity,
        'tax':tax,
        'grandTotal': grandTotal,
        'cartItems': cartItems
    }
    return render(request, 'cart.html', data)