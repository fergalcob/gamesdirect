from django.urls import path
from . import views

urlpatterns = [
        path('account/my_orders', views.my_orders, name='my_orders'),
]