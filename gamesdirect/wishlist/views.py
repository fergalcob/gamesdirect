from django.shortcuts import render
from store_pages.models import *
from wishlist.models import Wishlist
from django.db.models import Q


# Create your views here.

# View function for rendering the user's wishlist
def my_wishlist(request):
    if request.user.is_authenticated:
        # Retrieve the user's wishlist and render it
        my_wishlist, created = Wishlist.objects.get_or_create(owner=request.user)

        context = {"my_wishlist": my_wishlist}
        return render(request, "account/my_wishlist.html", context=context)


# View function to add games to the user's wishlist
def add_to_wishlist(request):
    # Create or retrieve the user's wishlist
    my_wishlist, created = Wishlist.objects.get_or_create(owner=request.user)
    my_wishlist.save()
    # Add the selected game to the wishlist
    my_wishlist.wishlist_items.add(
        Game.objects.get(
            Q(game_id=request.POST["item_id"])
            & Q(platform=request.POST["platform_id"])
        )
    )
    # Return to the index page after adding to wishlist
    return render(request, "store_pages/index.html")


# View function to remove games from the user's wishlist
def remove_from_wishlist(request):
    # Identify the game to remove
    game_to_remove = Game.objects.get(
        Q(game_id=request.POST["item_id"])
        & Q(platform=request.POST["platform_id"])
    )
    # Retrieve and update the user's wishlist
    my_wishlist = Wishlist.objects.get(owner=request.user)
    my_wishlist.wishlist_items.remove(game_to_remove)
    my_wishlist.save()

    # Return to the wishlist page after removing from wishlist
    return render(request, "account/my_wishlist.html")
