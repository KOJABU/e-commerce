from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('item/<int:item_id>/', views.detail, name = 'detail'),
    path('search/', views.search, name = 'search'),
    path('brand/', views.brand, name = 'brand'),
    path('category/', views.category, name = 'category'),
    path('producer/', views.country, name = 'producer'),
    path('add/', views.add_product, name='add'),
    path('change/<int:item_id>', views.change_product, name='change'),
    path('delete/<int:item_id>', views.delete_product, name='delete'),

]