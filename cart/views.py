from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from . models import Cart, CartItem
from product.models import Product, Variation
from django.contrib.auth.decorators import login_required


# Create your views here.
def get_cart_id(request): # private method
    cart = request.session.session_key
    # if there is no session then create a new one
    if not cart:
        cart = request.session.create()
    return cart  # returns the cart id

def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id) # fetch the product
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.object.get(product=product, variation_category__iexact =  key, variation_value__iexact = value)
                    product_variation.append(variation)
                except Exception as e:
                    print(e)

        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists # returns boolean
        if is_cart_item_exists:            
            cart_item = CartItem.objects.filter(product=product, user=current_user) # filtr the cart items, returns cart item object
            existing_variation_list = []
            ids = []
            for item in cart_item:
                existing_variation = item.variation.all()
                existing_variation_list.append(list(existing_variation) )
                ids.append(item.id)

            if product_variation in existing_variation_list:
                # increase cart item qty
                idx = existing_variation_list.index(product_variation)
                item_id = ids[idx]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                # create new cart item
                item = CartItem.objects.create(product=product,quantity=1, user=current_user)
                # add variation to the cart item
                if len(product_variation) > 0:
                    item.variation.clear()
                    item.variation.add(*product_variation)
                item.save()
        # when cart item doesnt exist, create new
        else:
            cart_item = CartItem.objects.create(
                product = product, 
                quantity = 1, 
                user = current_user,
            )
            # when new cart item is created add variation to it
            if len(product_variation) > 0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)
            cart_item.save()
        return redirect('cart')
    else:
        product_variation = []
        if request.method == 'POST':
            # color = request.POST.get('color')
            # size = request.POST.get('size')
            for item in request.POST:
                key = item
                value = request.POST[key]
                print(key, value)

                try:
                    variation = Variation.object.get(product=product, variation_category__iexact =  key, variation_value__iexact = value)
                    print('variation', variation)
                    product_variation.append(variation)
                except Exception as e:
                    print(e)

        try:
            cart = Cart.objects.get(cart_id=get_cart_id(request))  # get the cart_id present in session, and match cart_id with session_id
            print('CART:',cart, 'SESSION:', get_cart_id)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = get_cart_id(request)
            )
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists # returns boolean
        if is_cart_item_exists:
            #cart_item = CartItem.objects.get(product=product, cart=cart) # fetches the cart item
            #cart_item = CartItem.objects.create(product=product, quantity = 1,cart=cart) # creates a new cart item when variations is different
            
            cart_item = CartItem.objects.filter(product=product, cart=cart) # filtr the cart items, returns cart item object
            # existing variation -> from Db
            # current variation -> from the product_variation list
            # item_id -> from Db

            # if current variation is in exiting variation, increase cat item qty
            existing_variation_list = []
            ids = []
            for item in cart_item:
                existing_variation = item.variation.all()
                existing_variation_list.append(list(existing_variation) )
                ids.append(item.id)
            print(f'existing_variation_list:{existing_variation_list}, product_variation:{product_variation}')

            if product_variation in existing_variation_list:
                # increase cart item qty
                idx = existing_variation_list.index(product_variation)
                item_id = ids[idx]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                # create new cart item
                item = CartItem.objects.create(product=product,quantity=1, cart=cart)
                # add variation to the cart item
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
            # when new cart item is created add variation to it
            if len(product_variation) > 0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)
            cart_item.save()
        return redirect('cart')

def remove_from_cart(request, product_id, cart_item_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id = get_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart,id=cart_item_id)
        cart_item.delete()
        return redirect('cart')   
    except Exception as e:
        raise e


def decrement_cart_item(request, product_id, cart_item_id):
    
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id = get_cart_id(request))
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
        if request.user.is_authenticated:
            cartItems = CartItem.objects.filter(user=request.user)
        else:
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

@login_required(login_url='login')
def checkout(request, total=0, quantity=0, tax=0, grandTotal=0):
    try:
        cartItems = ''
        if request.user.is_authenticated: # for logged in users
            cartItems =  CartItem.objects.filter(user=request.user, is_active=True)
        else:
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
        'cart_items': cartItems
    }
    print('DATAAAA', data)
    return render(request, 'checkout.html', data)