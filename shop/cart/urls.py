from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.cart_checkout, name='cart_checkout'),
] 