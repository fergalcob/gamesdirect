from django.urls import path
from . import views
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views

urlpatterns = [
    re_path(r'add_to_wishlist', views.add_to_wishlist, name='add_to_wishlist'),
    re_path(r'remove_from_wishlist', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('account/my_wishlist', views.my_wishlist, name='my_wishlist'),
]
