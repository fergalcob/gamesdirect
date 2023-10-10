from django.urls import path
from . import views
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('games', views.games, name='games'),
    path('products/<str:pk>', views.products, name='products'),
    path('subscribe', views.subscribe_view, name='subscribe'),
    path('account/my_orders', views.my_orders, name='my_orders'),
    path('account/change_details', views.change_details, name='change_details'),
]