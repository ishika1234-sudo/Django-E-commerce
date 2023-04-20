
from django.urls import path
from . import views


urlpatterns = [
    path('', views.general_product_page, name='general_product_page' ),
    path('category/<slug:category_slug>/', views.product, name='product' ),
    #path('<slug:category_slug>/<slug:product_slug>/', views.product, name='products_in_wishlist' ),
    #path('category/<slug:category_slug>/<slug:product_slug>/', views.product, name='product' ),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_details, name='product_details' ),
    #path('category/<slug:category_slug>/<slug:product_slug>/product_filters', views.product_filters, name='product_filters' ),
    path('search/', views.search, name='search')
    
] 
