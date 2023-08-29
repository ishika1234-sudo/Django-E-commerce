from django.shortcuts import render,redirect
from .forms import RegistrationForm
from django.contrib import messages, auth
from django.contrib.auth import logout as logout_auth
from django.contrib.auth.decorators import login_required

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