import json  
import pytz
import logging
import random
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Prefetch
from datetime import datetime
from store_pages.models import *
from store_pages.forms import *
from django.db.models import Q
from django.http import HttpResponseRedirect
from mailchimp_marketing import Client
from django.conf import settings
from mailchimp_marketing.api_client import ApiClientError
from django.contrib import messages
from allauth.account.forms import AddEmailForm, ChangePasswordForm
from allauth.account.views import  PasswordChangeView, EmailView
from allauth.account.models import EmailAddress
from django.urls import reverse_lazy 
from allauth.utils import get_form_class
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO
import urllib.request
from django.core.paginator import Paginator

import secrets
import string

def index(request):
    on_sale = Game.objects.filter(sale_discount__gte=1).order_by("?")[:8]
    new_releases = Game.objects.filter().order_by("-first_release")[:8]
    top_rated = Game.objects.filter().order_by("-aggregated_rating")[:8]

    context = {
        "on_sale" : on_sale,
        "new_releases" : new_releases,
        "top_rated" : top_rated
    }
    return render(request,"store_pages/index.html", context=context)
