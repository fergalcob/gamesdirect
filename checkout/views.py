from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from store_pages.models import *
from django.views.generic.base import TemplateView
from datetime import datetime
import stripe
import secrets
import string
from django.contrib import messages
import mailchimp_transactional
from mailchimp_transactional.api_client import ApiClientError
import logging
from store_pages.views import index
