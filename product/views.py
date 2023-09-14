from django.shortcuts import render,  get_object_or_404, HttpResponse
from . models import Product, Brand
from category.models import Category
from cart.models import CartItem
from cart.views import get_cart_id
from wishlist.views import get_wishlist_id
from wishlist.models import Wishlist, Wishlist_Items
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

kwargs = {}
brandsList = []

def general_product_page(request):
    products = Product.objects.all().filter(is_available=True) 
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    no_of_products = products.count()
    
    data = {
        # 'products': products,
        'products': paged_products,
        'product_count': no_of_products,
        # 'in_wishlist':in_wishlist
    }
    return render(request, 'product.html', data)

# Create your views here.
def product(request, category_slug=None, product_slug=None):
    
    categories = None
    products = None
    in_wishlist = None
    brand = Brand.objects.all()
    brand_list = [ brands.brand_name for brands in brand]
    brand_dict = {brands.brand_name: brands.id for brands in brand }
    # print('branddddd ', list(brand), brand_list, brand_dict )

    if request.method == 'GET':
        kwargs.clear()
        brandsList.clear()

        if category_slug:
            categories = get_object_or_404(Category, slug = category_slug) # will return the category name else 404
            # print('CATEGORIES', category_slug, categories)
            products = Product.objects.all().filter(category=categories, is_available=True) 
            paginator = Paginator(products, 6)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            no_of_products = products.count()
            #in_wishlist = Wishlist_Items.objects.filter(wishlist__wishlist_id = get_wishlist_id(request), product = products).exists() 

        else:
            products = Product.objects.all().filter(is_available=True) 
            paginator = Paginator(products, 6)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            no_of_products = products.count()
        
        data = {
            # 'products': products,
            'products': paged_products,
            'product_count': no_of_products,
            'category':category_slug,
            'brands':brand,
            #'in_wishlist':in_wishlist
        }
        return render(request, 'product_type.html', data)
    
    if request.method == 'POST':
        categories = get_object_or_404(Category, slug = category_slug) # will return the category name else 404
        print('CATEGORIES', category_slug, categories)
        
        #-------------apply filters-------------------
        if 'sort_by' not in request.POST:
            for item in request.POST:
                key = item
                value = request.POST.get(key)
                if value:
                    kwargs['category'] = categories
                    if key == 'is_new':
                        if value == 'true':
                            kwargs['{0}'.format(key)] = True
                        else:
                            kwargs['{0}'.format(key)] = False
                    if key == 'min':
                        kwargs['{0}__{1}'.format('price', 'gte')] = value
                    if key == 'max':
                        kwargs['{0}__{1}'.format('price', 'lt')] = value
                    if key.capitalize() in brand_dict.keys():
                        print('keyeeee',key, value)
                        brandsList.append(brand_dict[value])
                        kwargs['brand__in'] = brandsList
                else:
                    kwargs['category'] = categories
            print('kwargs:', kwargs)
            products = Product.objects.filter(**kwargs)
        
        #-------------clear filters---------------------
        if 'price_filter' in request.POST:
            for key in list(kwargs):
                if key == 'price__gte':
                    kwargs.pop(key)
                if key == 'price__lt':
                    kwargs.pop(key)
            products = Product.objects.filter(**kwargs)
        if 'new_prod_filter' in request.POST:
            for key in list(kwargs):
                if key == 'is_new':
                    kwargs.pop(key)
            products = Product.objects.filter(**kwargs)
        if 'brand_filter' in request.POST:
            brandsList.clear()
            for key in list(kwargs):
                if key == 'brand__in':
                    kwargs.pop(key)
            products = Product.objects.filter(**kwargs)

        #-----------sorting---------------------------
        if 'sort_by' in request.POST:
            sort_by = request.POST['sort_by']
            if sort_by =='low':
                sort_by_val = 'price'
            elif sort_by =='high':
                sort_by_val = '-price'
            elif sort_by =='popular':
                sort_by_val = 'date_created'
            if not kwargs:
                products = Product.objects.all().filter(category=categories, is_available=True).order_by(sort_by_val)
            else:
                products = Product.objects.filter(**kwargs).order_by(sort_by_val)

        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        no_of_products = products.count()

        data = {
            # 'products': products,
            'products': paged_products,
            'product_count': no_of_products,
            'category':category_slug,
            'kwargs': kwargs,
            'brands':brand
            # 'in_wishlist':in_wishlist
        }            
        return render(request, 'product_type.html', data)


def product_details(request, category_slug, product_slug):
    try:
        if category_slug:
            categories = get_object_or_404(Category, slug=category_slug)
            products = Product.objects.get(category=categories, slug=product_slug)
            # single_product = Product.objects.get(category__slug = category_slug, slug = product_slug) # __ is the syntax to get access to the category slug first
            # print('single_product', single_product)
            in_cart = CartItem.objects.filter(cart__cart_id = get_cart_id(request), product = products).exists() # to first access cart then cart_id, as relation foreign key is there
            if request.user.is_authenticated:
                in_wishlist = Wishlist_Items.objects.filter(user=request.user, product = products).exists() 
            else:
                in_wishlist = Wishlist_Items.objects.filter(wishlist__wishlist_id = get_wishlist_id(request), product = products).exists() 

    except Exception as e:
        raise e
    data = {
        'single_product':products,
        'in_cart':in_cart,
        'in_wishlist':in_wishlist
    }
    return render(request, 'product_details.html', data)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET.get('keyword')
        if keyword:
            products = Product.objects.order_by('-date_created').filter(Q(product_description__icontains=keyword) | Q(product_name__icontains=keyword))
            no_of_products = products.count()
        data = {
            'products': products,
            'product_count': no_of_products
        }
    return render(request, 'product.html', data)