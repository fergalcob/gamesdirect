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

mailchimp = mailchimp_transactional.Client(
    api_key=settings.MAILCHIMP_TRANSACTIONAL_API,
)
logger = logging.getLogger(__name__)


# Create your views here.
@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)
    
@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        user_cart = CurrentCart.objects.get(owner=request.user)
        order_length = 16
        order_number_generator = ''.join(secrets.choice(string.ascii_uppercase + string.digits)for i in range(order_length))
        new_order, created = Orders.objects.get_or_create(order_number=order_number_generator)
        if created is True:
            new_order.owner_id = user_cart.owner
            new_order.order_items = user_cart.cart_items
            new_order.total_price = user_cart.total_price
            new_order.order_date = datetime.now()
            new_order.save()

        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=new_order.order_number,
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[{ 'price_data':{'product_data':{'name':'Order #' + str(new_order.order_number), 'description':'Payment to GamesDirect.Shop for Order #' + str(new_order.order_number) + '.'},'currency':'eur','unit_amount_decimal':user_cart.total_price.amount*100},'quantity':1}],          
            )

            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})
