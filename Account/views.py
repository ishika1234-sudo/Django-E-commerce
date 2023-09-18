from django.shortcuts import render,redirect
from .forms import RegistrationForm
from django.contrib import messages, auth
from django.contrib.auth import logout as logout_auth
from django.contrib.auth.decorators import login_required
from wishlist.views import get_wishlist_id
from wishlist.models import Wishlist,Wishlist_Items
from cart.models import Cart, CartItem
from cart.views import get_cart_id
import requests

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            #auth_login(request, user)
            messages.success(request, "Registration successful." )
            return redirect('register')
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
	
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'register.html', context)

def login(request):
    if request.method == 'POST':
        user_wish_list = []
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user:
            try:
                # get the list of wishlisted item by the user
                user_wishlist = Wishlist_Items.objects.filter(user=user)
                for items in user_wishlist:
                    user_wish_list.append(items.product.product_name)

                # check if there is anything in the wishlist when user is logged out
                wishlist = Wishlist.objects.get(wishlist_id=get_wishlist_id(request))
                is_wishlistItems_exists = Wishlist_Items.objects.filter(wishlist=wishlist, is_active=True).exists()
                if is_wishlistItems_exists:
                    wishlist_item = Wishlist_Items.objects.filter(wishlist=wishlist)
                    for item in wishlist_item:
                        # assign the user to the wishlist item, if user already hasn't wishlisted the item
                        if item.product.product_name not in user_wish_list:
                            item.user = user  
                            item.save()
            except:
                pass
            
            try:
                # check if anything is there inside the cart
                cart = Cart.objects.get(cart_id=get_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                # Getting the product variations by cart id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variation.all()
                        product_variation.append(list(variation))

                    # Get the cart items from the user to access his product variations
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variation.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except Exception as e:
                pass
            auth.login(request, user)

            url = request.META.get('HTTP_REFERER') 
            try:
                query = requests.utils.urlparse(url).query
                # next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('dashboard')

        else:
            messages.error(request, 'Invalid email or password')
            return redirect('login')
    return render(request, 'login.html')

@login_required(login_url='login') # this will check that you can only logout when you are logged in
def logout(request):
    logout_auth(request)
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'dashboard.html')