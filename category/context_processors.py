from .models import Category

# context processro is a python function 
def menu_links(request):
    links = Category.objects.all()
    print('LINK', dict(links=links))
    return dict(links=links)