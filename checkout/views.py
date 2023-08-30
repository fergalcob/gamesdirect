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

# Initialize Mailchimp client and logger
mailchimp = mailchimp_transactional.Client(api_key=settings.MAILCHIMP_TRANSACTIONAL_API)
logger = logging.getLogger(__name__)

# View function to retrieve Stripe configuration
@csrf_exempt
def stripe_config(request):
    if request.method == "GET":
        # Prepare and return Stripe configuration data
        stripe_config = {"publicKey": settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

# View function to create a checkout session for Stripe payment
@csrf_exempt
def create_checkout_session(request):
    if request.method == "GET":
        domain_url = "https://www.gamesdirect.shop/"
        stripe.api_key = settings.STRIPE_SECRET_KEY
        user_cart = CurrentCart.objects.get(owner=request.user)
        order_length = 16
        order_number_generator = "".join(
            secrets.choice(string.ascii_uppercase + string.digits)
            for i in range(order_length)
        )
        new_order, created = Orders.objects.get_or_create(
            order_number=order_number_generator
        )
        if created is True:
            # Create a new order if it doesn't exist
            new_order.owner_id = user_cart.owner
            new_order.order_items = user_cart.cart_items
            new_order.total_price = user_cart.total_price
            new_order.order_date = datetime.now()
            new_order.save()

        try:
            # Create a Stripe checkout session
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=new_order.order_number,
                success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=domain_url + "cancelled/",
                payment_method_types=["card"],
                mode="payment",
                line_items=[
                    {
                        "price_data": {
                            "product_data": {
                                "name": "Order #" + str(new_order.order_number),
                                "description": "Payment to GamesDirect.Shop"
                                " for Order #" + str(new_order.order_number) + ".",
                            },
                            "currency": "eur",
                            "unit_amount_decimal": user_cart.total_price.amount * 100,
                        },
                        "quantity": 1,
                    }
                ],
            )

            return JsonResponse({"sessionId": checkout_session["id"]})
        except Exception as e:
            return JsonResponse({"error": str(e)})

# View function to handle Stripe webhook events
@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        # Verify and parse the webhook event
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle different types of Stripe webhook events
    if event["type"] == "checkout.session.completed":
        # Handle successful checkout
        status_update = Orders.objects.get(
            order_number=event["data"]["object"]["client_reference_id"]
        )
        empty_cart = CurrentCart.objects.get(owner=status_update.owner_id)
        empty_cart.delete()
        for items in status_update.order_items["current_cart"]:
            items["activation_keys"] = []
            order_item = Game.objects.get(id=items["item_id"])
            for number_of_keys in range(0, items["item_quantity"]):
                key = order_item.keys_in_stock[number_of_keys]
                items["activation_keys"].append(key)
                order_item.keys_in_stock.pop(number_of_keys)
                order_item.save()
        status_update.order_status = "Completed"
        status_update.save()

        message = {
            "from_email": "support@gamesdirect.shop",
            "subject": "Your Order: " + status_update.order_number,
            "html": "<p>Hey there,</p> "
            "<p>We wish to let you know that your order("
            + status_update.order_number
            + ") has been completed. You can find your activation keys"
            " at the following URL:</p>"
            "<p>All the best,</p>"
            "<p>The GamesDirect Team</p>"
            '<a href="https://www.gamesdirect.shop">GamesDirect</a>',
            "to": [
                {"email": status_update.owner_id.email, "type": "to"},
            ],
        }
        try:
            response = mailchimp.messages.send(
                {
                    "message": message,
                }
            )
            return JsonResponse(
                {
                    "detail": "Email has been sent",
                    "response": response,
                }
            )
        except ApiClientError as error:
            return JsonResponse(
                {
                    "detail": "Something went wrong",
                    "error": error.text,
                }
            )

    elif event["type"] == "checkout.session.async_payment_succeeded":
        # Handle async payment success
        status_update = Orders.objects.get(
            order_number=event["data"]["object"]["client_reference_id"]
        )
        empty_cart = CurrentCart.objects.get(owner=status_update.owner_id)
        empty_cart.delete()
        for items in status_update.order_items["current_cart"]:
            items["activation_keys"] = []
            order_item = Game.objects.get(id=items["item_id"])
            for number_of_keys in range(0, items["item_quantity"]):
                key = order_item.keys_in_stock[number_of_keys]
                items["activation_keys"].append(key)
                order_item.keys_in_stock.pop(number_of_keys)
                order_item.save()
        status_update.order_status = "Completed"
        status_update.save()

        message = {
            "from_email": "support@gamesdirect.shop",
            "subject": "Your Order: " + status_update.order_number,
            "html": "<p>Hey there,</p> "
            "<p>We wish to let you know that your order("
            + status_update.order_number
            + ") has been completed. You can find your activation keys at"
            " the following URL:</p>"
            "<p>All the best,</p>"
            "<p>The GamesDirect Team</p>"
            '<a href="https://www.gamesdirect.shop">GamesDirect</a>',
            "to": [
                {"email": status_update.owner_id.email, "type": "to"},
            ],
        }
        try:
            response = mailchimp.messages.send(
                {
                    "message": message,
                }
            )
            return JsonResponse(
                {
                    "detail": "Email has been sent",
                    "response": response,
                }
            )
        except ApiClientError as error:
            return JsonResponse(
                {
                    "detail": "Something went wrong",
                    "error": error.text,
                }
            )
    elif event["type"] == "checkout.session.async_payment_failed":
        # Handle async payment failure
        status_update = Orders.objects.get(
            order_number=event["data"]["object"]["client_reference_id"]
        )
        status_update.order_status = "Payment Failed"
        status_update.save()

        message = {
            "from_email": "support@gamesdirect.shop",
            "subject": "Your Order: " + status_update.order_number,
            "html": "<p>Hey there,</p> "
            "<p>We wish to let you know that the payment for your order("
            + status_update.order_number
            + ") has failed. Your payment method has not been charged and"
            " your order has not been completed</p>"
            "<p>You can try again with a different payment method as"
            " your cart has been retained."
            "<p>All the best,</p>"
            "<p>The GamesDirect Team</p>"
            '<a href="https://www.gamesdirect.shop">GamesDirect</a>',
            "to": [
                {"email": status_update.owner_id.email, "type": "to"},
            ],
        }
        try:
            response = mailchimp.messages.send(
                {
                    "message": message,
                }
            )
            return JsonResponse(
                {
                    "detail": "Email has been sent",
                    "response": response,
                }
            )
        except ApiClientError as error:
            return JsonResponse(
                {
                    "detail": "Something went wrong",
                    "error": error.text,
                }
            )

    return HttpResponse(status=200)


# View function for successful payment page
def SuccessView(request):
    messages.add_message(
        request,
        messages.INFO,
        "Your payment was successful and your items will be delivered shortly.",
    )
    return redirect("index")


# View function for cancelled payment page
def CancelledView(request):
    messages.add_message(
        request, messages.INFO, "You have cancelled your payment."
    )
    return redirect("index")