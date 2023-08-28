"""
URL configuration for gamesdirect project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from store_pages.views import CustomPasswordChangeView, CustomEmailView 

urlpatterns = [
    path('admin/', admin.site.urls),
]

from django.urls import include

urlpatterns += [
    path('store_pages/', include('store_pages.urls')),
    path('accounts/password/change/', CustomPasswordChangeView.as_view(), name="account_change_password"),
    path('accounts/email/', CustomEmailView.as_view(), name="account_email"),
    path('accounts/', include('allauth.urls')),
    path('', include('checkout.urls')), # new
]

from django.views.generic import RedirectView
urlpatterns += [
    path('', RedirectView.as_view(url='store_pages/', permanent=True)),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

