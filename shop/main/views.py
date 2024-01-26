from msilib.schema import ListView
from django.shortcuts import get_object_or_404, render ,HttpResponse, redirect
from .models import *
from cart.forms import AddProductForm, CartNewProductForm
from .forms import AddProductForm2, ChangeProductForm
from cart.apikey import API_TOKEN
import requests
from django.contrib.gis.geoip2 import GeoIP2
from django.conf import settings
from django.db.models import Q
from django.core.cache import cache
# from django.views.decorators.cache import cache_page


# Create your views here.

# @cache_page
def index(request):
    # try:
    #     items = cache.get("items_cache")
    # except:
    #     items = Products.objects.all()
    # g = GeoIP2(settings.GEOIP_PATH)
    # # 149.115.178.2 - ip адрес, который есть в базе
    # a = g.country('149.115.178.2') # запрос к базе с данным айпи адресом
    # print(request.META.get('REMOTE_ADDR')) # адрес пользователя
    # print(a['country_name']) # вывод страны пользователя
    items = Products.objects.all()
    cart_product_form = CartNewProductForm
    brands = Brand.objects.all()
    categorys = Category.objects.all()
    producer = Producer.objects.all()
    return render(request,'main/index.html', {'items':items,
                                              'cart_product_form': cart_product_form,'brands': brands, 'categorys':  categorys, 'producer': producer})
            

def detail(request, item_id):
    try:
        item = Products.objects.get(id=item_id)
        cart_product_form = AddProductForm
        items = Products.objects.get(id=item_id)
        cart_product_form = AddProductForm
        api_key = API_TOKEN
        url1 = f'https://v6.exchangerate-api.com/v6/{api_key}/pair/USD/PLN'
        response = requests.get(url1)
        data = response.json()
        cv =  data.get('conversion_rate')
        items.price *=cv
        items.price = round(items.price)
    except:
        return redirect('/')
    return render(request, 'main/detail.html', {'item':item,
                                                'cart_product_form':cart_product_form,'items': items})
    
    
def brand(request):
    if request.method == "GET":
        brands = Brand.objects.all()
        query = request.GET.get('brands_shoes')
        brand_instance = get_object_or_404(Brand, name=query)
        brand_id = brand_instance.id
        items = Products.objects.filter(brand=brand_id)
        categorys = Category.objects.all()
        producer = Producer.objects.all()
        cart_product_form = CartNewProductForm
    return render(request, 'main/index.html',{'query': query,'brand_id': brand_id,'items': items,'cart_product_form': cart_product_form, 
                                              'brands': brands, 'categorys': categorys,'producer': producer,})



def category(request):
    if request.method == "GET":
        categorys = Category.objects.all()
        query = request.GET.get('category_shoes')
        category_instance = get_object_or_404(Category, name=query)
        category_id = category_instance.id
        items = Products.objects.filter(category=category_id)
        brands = Brand.objects.all()
        producer = Producer.objects.all()
        cart_product_form = CartNewProductForm
    return render(request, 'main/index.html',{'query': query,'category_id': category_id,'items': items,'cart_product_form': cart_product_form,
                                              'categorys':  categorys,'brands': brands,'producer': producer,})

def country(request):
    producer = Producer.objects.all()
    brands = Brand.objects.all()
    categorys = Category.objects.all()
    cart_product_form = CartNewProductForm()
    query = request.GET.get('country_shoes')
    print(query,'RFERECECFCEGHE')
    if query:
        producer_instance = get_object_or_404(Producer, name=query)
        producer_id = producer_instance.id
        items = Products.objects.filter(producer=producer_id)
    else:
        producer_id = None
        items = Products.objects.none()  # or however you want to handle this

    return render(request, 'main/index.html', {
        'query': query,
        'producer': producer,
        'producer_id': producer_id,
        'items': items,
        'cart_product_form': cart_product_form,
        'categorys': categorys,
        'brands': brands
    })
    
    

def search(request):
    items = []
    if request.method == "GET":
        query = request.GET.get('q')
        # if query == '':
        #     query = 'None'
        items = Products.objects.filter(Q(name__icontains=query)) 
        cart_product_form = CartNewProductForm
    return render(request,'main/search.html', {'query': query, 'items': items,'cart_product_form': cart_product_form})



def add_product(request):
    if request.method == 'POST':
        add_form = AddProductForm2(request.POST, request.FILES)
        if add_form.is_valid():
            photo1 = request.FILES['photo'] if 'photo' in request.FILES else 'photo/2023/12/26/empty.png'
            
            Products(
                name=add_form.cleaned_data['name'],
                price=add_form.cleaned_data['price'],
                photo=photo1,
                pre_description=add_form.cleaned_data['pre_description'],
                description=add_form.cleaned_data['description'],
                category=Category.objects.get(id=add_form.cleaned_data['category']),
                brand=Brand.objects.get(id=add_form.cleaned_data['brand']),
                producer=Producer.objects.get(id=add_form.cleaned_data['producer'])
            ).save()
    else:
        pass
        
    add_form = AddProductForm2()
    return render(request, 'main/add.html', {'add_form': add_form})





def change_product(request, item_id):
    try:
        product = Products.objects.get(id=item_id)
    except Products.DoesNotExist:
        return redirect('/')

    if request.method == "POST":
        change_form = ChangeProductForm(request.POST, request.FILES)
        if change_form.is_valid():
            product.name = change_form.cleaned_data['name']
            product.price = change_form.cleaned_data['price']
            product.pre_description = change_form.cleaned_data['pre_description']
            product.description = change_form.cleaned_data['description']
            product.category = Category.objects.get(id=change_form.cleaned_data['category'])
            product.brand = Brand.objects.get(id=change_form.cleaned_data['brand'])
            product.producer = Producer.objects.get(id=change_form.cleaned_data['producer'])

            if 'photo' in request.FILES:
                product.photo = request.FILES['photo']

            product.save()
            return redirect('main:index')
    else:
        initial_data = {
            'name': product.name,
            'price': product.price,
            'pre_description': product.pre_description,
            'description': product.description,
            'category': product.category.id,
            'brand': product.brand.id,
            'producer': product.producer.id,
        }
        change_form = ChangeProductForm(initial=initial_data)

    return render(request, 'main/change.html', {'change_form': change_form, 'item_id': item_id})

def delete_product(request, item_id):
    product = get_object_or_404(Products, id=item_id)
    product.delete()
    return render(request, 'main/index.html') 


# def change_product(request, item_id):
#     try:
#         product = Products.objects.get(id=item_id)
#         if request.method == "POST":   
#             change_form = ChangeProductForm(request.FILES)
#             product.name = request.POST.get('name')
#             product.price = request.POST.get('price')
#             product.pre_description = request.POST.get('pre_description')
#             product.description = request.POST.get('description')
#             product.category = Category.objects.get(id=request.POST.get('category'))
#             product.brand = Brand.objects.get(id=request.POST.get('brand'))
#             product.producer = Producer.objects.get(id=request.POST.get('producer'))
#             product.save()
#             return redirect('main:index')  
#     except Products.DoesNotExist:
#         # Handle the case where the product does not exist
#         return redirect('/')
    
#     # Initialize the form with the current product data
#     initial_data = {
#         'name': product.name,
#         'price': product.price,
#         'pre_description': product.pre_description,
#         'description': product.description,
#         'category': product.category.id,
#         'brand': product.brand.id,
#         'producer': product.producer.id,
#     }
#     change_form = ChangeProductForm(initial=initial_data)

#     return render(request, 'main/change.html', {'change_form': change_form, 'item_id': item_id})


 



