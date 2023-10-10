from django.urls import path
from . import views
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'add_to_cart', views.add_to_cart, name='add_to_cart'),
    re_path(r'remove_from_cart', views.remove_from_cart, name='remove_from_cart'),
    re_path(r'update_cart', views.update_cart, name='update_cart'),
    path('games', views.games, name='games'),
    path('products/<str:pk>', views.products, name='products'),
    path('subscribe', views.subscribe_view, name='subscribe'),
    path('account/my_orders', views.my_orders, name='my_orders'),
    path('account/change_details', views.change_details, name='change_details'),
]