from django.urls import path
from . import views
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views


urlpatterns = [
    re_path(r'add_to_cart', views.add_to_cart, name='add_to_cart'),
    re_path(r'remove_from_cart', views.remove_from_cart, name='remove_from_cart'),
    re_path(r'update_cart', views.update_cart, name='update_cart'),
]