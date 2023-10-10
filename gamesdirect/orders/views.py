from django.shortcuts import render
from orders.models import Orders

# Create your views here.

# View function for displaying user's order history
def my_orders(request):
    if request.user.is_authenticated:
        my_order_list = Orders.objects.filter(owner_id=request.user)

    context = {"my_orders": my_order_list}

    return render(request, "store_pages/my_orders.html", context=context)