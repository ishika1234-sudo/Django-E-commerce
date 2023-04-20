from django.http import HttpResponse
from django.shortcuts import render
from product.models import Product

def home(request):
    #return HttpResponse('Home page')
    products = Product.objects.all().filter(is_available =True) 
    is_new = Product.objects.all().filter(is_new =True) 
    data = {
        'products': products, 
        'is_new': is_new
    }
    return render(request, 'home.html', data)