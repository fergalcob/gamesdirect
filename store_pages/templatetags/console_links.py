from django import template
from store_pages.models import *
from store_pages.forms import SignUpForm
from django.contrib.messages import get_messages
from django.db.models import Q



register = template.Library()

@register.simple_tag
def get_consoles():
    all_consoles = Console.objects.all()
    return all_consoles

@register.simple_tag
def get_cart(request):
    my_cart = CurrentCart.objects.filter(owner=request.user)
    return my_cart

@register.simple_tag
def check_wishlist(user, game_value,platform_value):
    game_to_check = Game.objects.get(Q(game_id=game_value) & Q(platform=platform_value))

    if user.is_authenticated:
        return Wishlist.objects.filter(Q(owner=user) & Q(wishlist_items__game_id=game_to_check.game_id) & Q(wishlist_items__platform=game_to_check.platform)).exists()
