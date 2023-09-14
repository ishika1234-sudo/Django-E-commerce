from django.shortcuts import render,redirect
from .forms import RegistrationForm
from django.contrib import messages, auth
from django.contrib.auth import logout as logout_auth
from django.contrib.auth.decorators import login_required
from wishlist.views import get_wishlist_id
from wishlist.models import Wishlist,Wishlist_Items

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
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user:
            try:
                # first check if there is anything in the wishlist
                wishlist = Wishlist.objects.get(wishlist_id=get_wishlist_id(request))
                is_wishlistItems_exists = Wishlist_Items.objects.filter(wishlist=wishlist, is_active=True).exists()
                if is_wishlistItems_exists:
                    wishlist_item = Wishlist_Items.objects.filter(wishlist=wishlist)
                    for item in wishlist_item:
                        item.user = user  # assign the user to the wishlist item
                        item.save()

            except:
                pass
            auth.login(request, user)
            #messages.success(request, 'You are now logged in')
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