from django import template
from store_pages.models import Game
from wishlist.models import Wishlist

@register.simple_tag
def check_wishlist(user, game_value,platform_value):
    game_to_check = Game.objects.get(Q(game_id=game_value) & Q(platform=platform_value))

    if user.is_authenticated:
        return Wishlist.objects.filter(Q(owner=user) & Q(wishlist_items__game_id=game_to_check.game_id) & Q(wishlist_items__platform=game_to_check.platform)).exists()
