from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from . models import Cart, CartItem
from product.models import Product

# Create your views here.
def get_cart_id(request): # private method
    cart = request.session.session_key
    # if there is no session then create a new one
    if not cart:
        cart = request.session.create()
    return cart  # returns the cart id

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id) # fetch the product
    try:
        cart = Cart.objects.get(cart_id=get_cart_id(request))  # get the cart_id present in session, and match cart_id with session_id
        print('CART:',cart, 'SESSION:', get_cart_id)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = get_cart_id(request)
        )
    cart.save()
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart) # fetches the cart item
        #increment the cart item qty by 1
        cart_item.quantity += 1
        cart_item.save()
    # when cart item doesnt exist, create new
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product, 
            quantity = 1, 
            cart = cart,
        )
        cart_item.save()
    # return HttpResponse(cart_item.product)
    # exit()
    #return user to cart page
    return redirect('cart')

def remove_from_cart(request, product_id):
    try:
        cart = Cart.objects.get(cart_id = get_cart_id(request))
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.delete()
        return redirect('cart')   
    except Exception as e:
        raise e


def decrement_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id = get_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:    
        cart_item.delete()
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