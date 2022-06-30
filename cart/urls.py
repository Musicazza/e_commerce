from django.urls import path
from . import views
from django.conf.urls import url,include


app_name = 'cart'

urlpatterns = [
    path(r'', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('', include("django.contrib.auth.urls")),
    
]