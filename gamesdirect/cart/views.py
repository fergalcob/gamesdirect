from django.shortcuts import render
from store_pages.models import *
from .models import CurrentCart
import json
from django.http import JsonResponse, Http404



# View function for adding products to the cart
def add_to_cart(request):
    # Creating or retrieving the user's cart
    test_cart, created = CurrentCart.objects.get_or_create(owner=request.user)
    add_product = Game.objects.get(id=request.POST["item_id"])
    cover = Cover.objects.get(game_ids=add_product)
    console = Console.objects.get(console_id=add_product.platform)
    print('hello')
    # Handling the addition of products to the cart
    if created is True:
        test_cart.cart_items = {"current_cart": []}
        cart_items = {
            "item_id": add_product.id,
            "item_quantity": int(request.POST["quantity"]),
            "item_price": str(add_product.sale_price.amount),
            "item_name": add_product.name,
            "item_thumbnail": cover.cover_thumb_resized.url,
            "item_slug": add_product.slug,
            "item_platform": add_product.platform,
            "item_console": console.name,
        }
        print(cart_items)
        test_cart.cart_items["current_cart"].append(cart_items)
    else:
        # Check if the cart already contains the product
        cart_item_test = next(
            (
                item
                for item in test_cart.cart_items["current_cart"].copy()
                if item["item_id"] == add_product.id
            ),
            None,
        )
        if cart_item_test is not None:
            print(cart_item_test["item_quantity"])
            cart_item_test["item_quantity"] = (
                int(cart_item_test["item_quantity"]) + 1
            )
            print(cart_item_test)
        else:
            # Adding the product to the cart
            cart_items = {
                "item_id": add_product.id,
                "item_quantity": int(request.POST["quantity"]),
                "item_price": str(add_product.sale_price.amount),
                "item_name": add_product.name,
                "item_thumbnail": cover.url_thumbnail,
                "item_slug": add_product.slug,
                "item_platform": add_product.platform,
                "item_console": console.name,
            }
            test_cart.cart_items["current_cart"].append(cart_items)

    # Updating the cart's total price and saving changes
    test_cart.total_price = calculate_total(
        test_cart.cart_items["current_cart"]
    )
    test_cart.save()

    # Returning a JSON response
    return JsonResponse(
        {
            "current_total_json": list("current_total"),
            "current_cart": list("product_list"),
        }
    )

# View function for removing an item from the cart
def remove_from_cart(request):
    remove_item = request.POST["item_id"]
    get_user_cart = CurrentCart.objects.get(owner=request.user)
    cart_item_confirmation = next(
        (
            item
            for item in get_user_cart.cart_items["current_cart"].copy()
            if item["item_id"] == int(remove_item)
        ),
        None,
    )
    get_user_cart.cart_items["current_cart"].remove(cart_item_confirmation)
    get_user_cart.total_price = calculate_total(
        get_user_cart.cart_items["current_cart"]
    )
    get_user_cart.save()
    return JsonResponse(
        {
            "current_total_json": list("current_total"),
            "current_cart": list("product_list"),
        }
    )


# View function for updating the cart
def update_cart(request):
    new_quantity = request.POST["item_quantity"]
    print(new_quantity)
    if int(new_quantity) == 0:
        remove_from_cart(request)  # If quantity is 0, remove item from cart
    else:
        update_item = request.POST["item_id"]
        get_user_cart = CurrentCart.objects.get(owner=request.user)
        get_item_stock = Game.objects.get(id=request.POST["item_id"])
        cart_item_confirmation = next(
            (
                item
                for item in get_user_cart.cart_items["current_cart"].copy()
                if item["item_id"] == int(update_item)
            ),
            None,
        )
        if int(new_quantity) <= len(get_item_stock.keys_in_stock):
            cart_item_confirmation["item_quantity"] = new_quantity
        get_user_cart.total_price = calculate_total(
            get_user_cart.cart_items["current_cart"]
        )
        get_user_cart.save()
    return JsonResponse(
        {
            "current_total_json": list("current_total"),
            "current_cart": list("product_list"),
        }
    )


# Function to calculate the total price of items in the cart
def calculate_total(cart_status):
    price_calculation = 0
    for products in cart_status:
        price_calculation += float(products["item_price"]) * float(
            products["item_quantity"]
        )
    return price_calculation