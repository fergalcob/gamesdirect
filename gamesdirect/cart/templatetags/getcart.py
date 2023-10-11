from django import template
from cart.models import CurrentCart

register = template.Library()

@register.simple_tag
def get_cart(request):
    my_cart = CurrentCart.objects.filter(owner=request.user)
    return my_cart