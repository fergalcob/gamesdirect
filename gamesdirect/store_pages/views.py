# Import necessary libraries and modules
import json
import pytz
import logging
import random
from django.shortcuts import render, redirect
from django.http import JsonResponse, Http404
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
from allauth.account.views import PasswordChangeView, EmailView
from allauth.account.models import EmailAddress
from django.urls import reverse_lazy
from allauth.utils import get_form_class
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO
import urllib.request
from django.core.paginator import Paginator

# Generate secure random strings
import secrets
import string

# Configure logging
logger = logging.getLogger(__name__)

# Load data from a JSON file
with open("store_pages/pc_response.json", encoding="utf-8") as f:
    data = json.load(f)


# Custom view for changing passwords
class CustomPasswordChangeView(PasswordChangeView):
    # Define the template for rendering
    template_name = "account/change_details.html"
    # Define the URL to redirect to upon success
    success_url = reverse_lazy("change_details")

    # Handle invalid form submission
    def form_invalid(self, form):
        password_change_form = form
        email_form = AddEmailForm()
        # Render the template with relevant context data
        return render(
            self.request,
            self.template_name,
            {
                "password_change_form": password_change_form,
                "email_form": email_form,
                "emailaddresses": list(
                    EmailAddress.objects.filter(
                        user=self.request.user
                    ).order_by("email")
                ),
                # Retrieve and display various email addresses
                # associated with the user
                "new_emailaddress": EmailAddress.objects.get_new(
                    self.request.user
                ),
                "current_emailaddress": EmailAddress.objects.get_verified(
                    self.request.user
                ),
            },
        )


# Custom view for changing email addresses
class CustomEmailView(EmailView):
    # Define the template for rendering
    template_name = "account/change_details.html"
    # Define the URL to redirect to upon success
    success_url = reverse_lazy("change_details")

    # Handle invalid form submission
    def form_invalid(self, form):
        email_form = form
        password_change_form = ChangePasswordForm()
        # Render the template with relevant context data
        return render(
            self.request,
            self.template_name,
            {
                "password_change_form": password_change_form,
                "email_form": email_form,
                "emailaddresses": list(
                    EmailAddress.objects.filter(
                        user=self.request.user
                    ).order_by("email")
                ),
                # Retrieve and display various email
                # addresses associated with the user
                "new_emailaddress": EmailAddress.objects.get_new(
                    self.request.user
                ),
                "current_emailaddress": EmailAddress.objects.get_verified(
                    self.request.user
                ),
            },
        )


# Function for adding game data to the database
def game_addition(data):
    for games in data:
        for platforms in games["game"]["platforms"]:
            if platforms in [6, 130, 167, 169]:
                # Create a new Game object or retrieve an existing one
                new_game, created = Game.objects.get_or_create(
                    game_id=games["game"]["id"], platform=platforms
                )
                if created is True:
                    # Populate various attributes of the Game object
                    new_game.game_id = games["game"]["id"]
                    new_game.aggregated_rating_count = games["game"][
                        "aggregated_rating_count"
                    ]
                    new_game.platform = platforms
                    new_game.first_release = datetime.fromtimestamp(
                        games["game"]["first_release_date"], tz=pytz.UTC
                    )
                    new_game.genres = games["game"]["genres"]
                    new_game.slug = games["game"]["slug"]
                    new_game.summary = games["game"]["summary"]
                    new_game.name = games["game"]["name"]
                    new_game.aggregated_rating = games["game"][
                        "aggregated_rating"
                    ]
                    new_game.save()

                    # Create or retrieve a Cover
                    # object associated with the game
                    new_game_cover, created = Cover.objects.get_or_create(
                        cover_id=games["game"]["cover"]["id"]
                    )
                    if created is True:
                        # Populate attributes of the Cover object
                        new_game_cover.url = games["game"]["cover"]["url"]
                        new_game_cover.url_thumbnail = games["game"]["cover"][
                            "url"
                        ].replace("t_original", "t_thumb")
                        new_game_cover.cover_id = games["game"]["cover"]["id"]
                        new_game_cover.save()
                        new_game_cover.game_ids.add(new_game)
                        # Download and process cover images
                        print("https:" + new_game_cover.url_thumbnail)
                        urllib.request.urlretrieve(
                            new_game_cover.url_thumbnail,
                            str(new_game_cover.cover_id) + "_thumb.png",
                        )
                        f = Image.open(
                            str(new_game_cover.cover_id) + "_thumb.png"
                        )
                        upload_file_stream = BytesIO()
                        f.save(upload_file_stream, format="webp")
                        upload_file_stream.seek(0)
                        new_game_cover.cover_thumb_resized = ContentFile(
                            upload_file_stream.getvalue(),
                            "cover_thumb"
                            + str(new_game_cover.cover_id)
                            + ".webp",
                        )
                        f.close()
                        urllib.request.urlretrieve(
                            new_game_cover.url,
                            str(new_game_cover.cover_id) + ".png",
                        )
                        f = Image.open(str(new_game_cover.cover_id) + ".png")
                        upload_file_stream = BytesIO()
                        f.save(upload_file_stream, format="webp")
                        upload_file_stream.seek(0)
                        new_game_cover.cover_large_resized = ContentFile(
                            upload_file_stream.getvalue(),
                            "cover_large"
                            + str(new_game_cover.cover_id)
                            + ".webp",
                        )
                        new_game_cover.cover_mobile_resized = ContentFile(
                            upload_file_stream.getvalue(),
                            "cover_mobile"
                            + str(new_game_cover.cover_id)
                            + ".webp",
                        )
                        f.close()
                        new_game_cover.save()
                    else:
                        new_game_cover.game_ids.add(new_game)

                    # Handle videos associated with the game
                    try:
                        for videos in games["game"]["videos"]:
                            (
                                new_game_videos,
                                created,
                            ) = Videos.objects.get_or_create(
                                videos_id=videos["id"]
                            )
                            if created is True:
                                new_game_videos.videos_id = videos["id"]
                                new_game_videos.video_id = videos["video_id"]
                                new_game_videos.save()
                                new_game_videos.game_ids.add(new_game)
                    except KeyError:
                        continue

                    # Handle screenshots associated with the game
                    try:
                        for screenshots in games["game"]["screenshots"]:
                            (
                                new_game_screenshots,
                                created,
                            ) = Screenshots.objects.get_or_create(
                                screenshots_id=screenshots["id"]
                            )
                            if created is True:
                                new_game_screenshots.screenshots_id = (
                                    screenshots["id"]
                                )
                                new_game_screenshots.url = screenshots["url"]
                                new_game_screenshots.save()
                                new_game_screenshots.game_ids.add(new_game)
                                urllib.request.urlretrieve(
                                    new_game_screenshots.url,
                                    str(new_game_screenshots.screenshots_id)
                                    + ".png",
                                )
                                f = Image.open(
                                    str(new_game_screenshots.screenshots_id)
                                    + ".png"
                                )
                                upload_file_stream = BytesIO()
                                f.save(upload_file_stream, format="webp")
                                upload_file_stream.seek(0)
                                new_game_screenshots.screen_large_resized = (
                                    ContentFile(
                                        upload_file_stream.getvalue(),
                                        "screen_large"
                                        + str(
                                            new_game_screenshots.screenshots_id
                                        )
                                        + ".webp",
                                    )
                                )
                                new_game_screenshots.screen_mobile_resized = (
                                    ContentFile(
                                        upload_file_stream.getvalue(),
                                        "screen_mobile"
                                        + str(
                                            new_game_screenshots.screenshots_id
                                        )
                                        + ".webp",
                                    )
                                )
                                f.close()
                                new_game_screenshots.save()
                            else:
                                new_game_screenshots.game_ids.add(new_game)
                    except KeyError:
                        continue

                    # Handle involved companies associated with the game
                    for involved_companies in games["game"][
                        "involved_companies"
                    ]:
                        for companies in involved_companies:
                            (
                                new_game_company,
                                created,
                            ) = Company.objects.get_or_create(
                                company_id=involved_companies["company"]["id"]
                            )
                            if created is True:
                                new_game_company.company_id = (
                                    involved_companies["company"]["id"]
                                )
                                new_game_company.name = involved_companies[
                                    "company"
                                ]["name"]
                                new_game_company.slug = involved_companies[
                                    "company"
                                ]["slug"]
                                new_game_company.save()

                            new_game_involved_companies = Involved_companies()
                            (new_game_involved_companies
                             .involved_companies_id) = involved_companies[
                                "id"
                            ]
                            new_game_involved_companies.publisher = (
                                involved_companies["publisher"]
                            )
                            new_game_involved_companies.developer = (
                                involved_companies["developer"]
                            )
                            new_game_involved_companies.company_id = (
                                new_game_company
                            )
                            new_game_involved_companies.save()
                            new_game_involved_companies.game_ids.add(new_game)


# Function to add genres to the database
def genre_addition(data):
    for genres in data:
        # Create or retrieve a Genre object
        new_genre, created = Genres.objects.get_or_create(
            genre_id=genres["id"]
        )
        if created is True:
            # Populate attributes of the Genre object
            new_genre.genre_id = genres["id"]
            new_genre.slug = genres["slug"]
            new_genre.name = genres["name"]
            new_genre.save()


# Function to assign random keys to games in stock
def stock_assignment():
    # Retrieve random games from the database
    game_keys = Game.objects.filter().order_by("?")[:75]
    for games in game_keys:
        random_amount = random.randint(1, 30)
        for keys in range(random_amount):
            # Generate a random order number
            order_length = 4
            order_number_generator = (
                "".join(
                    secrets.choice(string.ascii_uppercase + string.digits)
                    for i in range(order_length)
                )
                + "-"
                + "".join(
                    secrets.choice(string.ascii_uppercase + string.digits)
                    for i in range(order_length)
                )
                + "-"
                + "".join(
                    secrets.choice(string.ascii_uppercase + string.digits)
                    for i in range(order_length)
                )
                + "-"
                + "".join(
                    secrets.choice(string.ascii_uppercase + string.digits)
                    for i in range(order_length)
                )
            )
            # Append the generated order number to keys_in_stock
            games.keys_in_stock.append(order_number_generator)
            games.save()


# Function to generate sale discounts for random games
def sale_generation():
    # Retrieve random games from the database
    random_games = Game.objects.filter().order_by("?")[:40]
    for each_game in random_games:
        # Assign a random sale discount to each game
        each_game.sale_discount = random.randint(1, 50)
        each_game.save()


# View function for rendering the index page
def index(request):
    # Retrieve games on sale, new releases, and top rated games
    on_sale = Game.objects.filter(sale_discount__gte=1).order_by("?")[:8]
    new_releases = Game.objects.filter().order_by("-first_release")[:8]
    top_rated = Game.objects.filter().order_by("-aggregated_rating")[:8]

    context = {
        "on_sale": on_sale,
        "new_releases": new_releases,
        "top_rated": top_rated,
    }
    # Render the index page with the retrieved game data
    return render(request, "store_pages/index.html", context=context)


# View function for displaying games based on various
# filters and sorting options
def games(request):
    genres = Genres.objects.all()

    # Check if filtering by platform
    if "platform" in request.GET:
        referrer = "platform"
        chosen_selector = Console.objects.get(slug=request.GET["platform"])

        # Check if filtering by genre
        if "filter" in request.GET:
            chosen_filter = Genres.objects.get(slug=request.GET["filter"])

            # Check if sorting option is specified
            if "sort" in request.GET:
                chosen_sort = request.GET["sort"]
                if "dir" in request.GET:
                    chosen_dir = request.GET["dir"]
                    if chosen_dir == "desc":
                        chosen_sort = f"-{chosen_sort}"
                    # Query games based on platform, genre, and sorting
                    game_list = (
                        Game.objects.filter(
                            platform=chosen_selector.console_id
                        )
                        .filter(genres__contains=[chosen_filter.genre_id])
                        .order_by(chosen_sort)
                    )
            else:
                # Query games based on platform and genre
                game_list = Game.objects.filter(
                    platform=chosen_selector.console_id
                ).filter(genres__contains=[chosen_filter.genre_id])

        else:
            # Handling sorting without filtering
            if "sort" in request.GET:
                chosen_sort = request.GET["sort"]
                if "dir" in request.GET:
                    chosen_dir = request.GET["dir"]
                    if chosen_dir == "desc":
                        chosen_sort = f"-{chosen_sort}"
                    # Query games based on platform and sorting
                    game_list = Game.objects.filter(
                        platform=chosen_selector.console_id
                    ).order_by(chosen_sort)
            else:
                # Query games based on platform
                game_list = Game.objects.filter(
                    platform=chosen_selector.console_id
                ).prefetch_related("cover_set")
    elif "genres" in request.GET:
        # Filtering by genre
        referrer = "genres"
        chosen_selector = Genres.objects.get(slug=request.GET["genres"])

        # Check if filtering by genre
        if "filter" in request.GET:
            chosen_filter = Genres.objects.get(slug=request.GET["filter"])

            # Check if sorting option is specified
            if "sort" in request.GET:
                chosen_sort = request.GET["sort"]
                if "dir" in request.GET:
                    chosen_dir = request.GET["dir"]
                    if chosen_dir == "desc":
                        chosen_sort = f"-{chosen_sort}"
                    # Query games based on genre, filtered genre, and sorting
                    game_list = (
                        Game.objects.filter(
                            genres__contains=[chosen_selector.genre_id]
                        )
                        .filter(genres__contains=[chosen_filter.genre_id])
                        .order_by(chosen_sort)
                    )
            else:
                # Query games based on genre and filtered genre
                game_list = Game.objects.filter(
                    genres__contains=[chosen_selector.genre_id]
                ).filter(genres__contains=[chosen_filter.genre_id])

        else:
            # Handling sorting without filtering
            if "sort" in request.GET:
                chosen_sort = request.GET["sort"]
                if "dir" in request.GET:
                    chosen_dir = request.GET["dir"]
                    if chosen_dir == "desc":
                        chosen_sort = f"-{chosen_sort}"
                    # Query games based on genre and sorting
                    game_list = Game.objects.filter(
                        genres__contains=[chosen_selector.genre_id]
                    ).order_by(chosen_sort)
            else:
                # Query games based on genre
                game_list = Game.objects.filter(
                    genres__contains=[chosen_selector.genre_id]
                )
    elif "company" in request.GET:
        # Filtering by company
        referrer = "company"
        chosen_selector = Company.objects.get(slug=request.GET["company"])

        # Query games associated with the selected company
        games_from_company = Involved_companies.objects.filter(
            company_id=chosen_selector
        )
        company_games_list = []
        for each_game in games_from_company:
            for individual_games in each_game.game_ids.all():
                company_games_list.append(individual_games.game_id)

        # Check if filtering by genre
        if "filter" in request.GET:
            chosen_filter = Genres.objects.get(slug=request.GET["filter"])

            # Check if sorting option is specified
            if "sort" in request.GET:
                chosen_sort = request.GET["sort"]
                if "dir" in request.GET:
                    chosen_dir = request.GET["dir"]
                    if chosen_dir == "desc":
                        chosen_sort = f"-{chosen_sort}"
                    # Query games based on filtered company, genre, and sorting
                    game_list = (
                        Game.objects.filter(game_id__in=company_games_list)
                        .filter(genres__contains=[chosen_filter.genre_id])
                        .order_by(chosen_sort)
                    )
            else:
                # Query games based on filtered company and genre
                game_list = Game.objects.filter(
                    game_id__in=company_games_list
                ).filter(genres__contains=[chosen_filter.genre_id])

        else:
            # Handling sorting without filtering
            if "sort" in request.GET:
                chosen_sort = request.GET["sort"]
                if "dir" in request.GET:
                    chosen_dir = request.GET["dir"]
                    if chosen_dir == "desc":
                        chosen_sort = f"-{chosen_sort}"
                    # Query games based on filtered company and sorting
                    game_list = Game.objects.filter(
                        game_id__in=company_games_list
                    ).order_by(chosen_sort)
            else:
                # Query games based on filtered company
                game_list = Game.objects.filter(game_id__in=company_games_list)
    elif request.method == "POST":
        # Handling search via POST method
        chosen_selector = "search"
        referrer = None
        search_query = request.POST["search_query"]
        print(search_query)
        # Query games based on search query
        game_list = Game.objects.filter(name__icontains=search_query)
    else:
        raise Http404

    # Pagination handling
    page_number = request.GET.get("page")
    if page_number is None or page_number == "":
        page_number = 1
    paginator = Paginator(game_list, 16)
    page_obj = paginator.page(page_number)
    context = {
        "page_obj": page_obj,
        "chosen_selector": chosen_selector,
        "genres": genres,
        "referrer": referrer,
    }
    return render(request, "store_pages/platform.html", context=context)


# View function for displaying product details
def products(request, pk):
    # Retrieving platform and product details
    platform_id = request.GET["platform"]
    product = Game.objects.get(Q(slug=pk) & Q(platform=platform_id))

    # Retrieving related product data
    product_videos = Videos.objects.filter(game_ids__game_id=product.game_id)
    product_screenshots = Screenshots.objects.filter(
        game_ids__game_id=product.game_id
    )
    product_cover = Cover.objects.get(
        Q(game_ids__game_id=product.game_id)
        & Q(game_ids__platform=platform_id)
    )
    product_genres = Genres.objects.filter(genre_id__in=product.genres)
    product_publisher = Involved_companies.objects.filter(
        Q(game_ids__game_id=product.game_id)
        & Q(game_ids__platform=platform_id)
        & Q(publisher=True)
    )
    product_developer = Involved_companies.objects.filter(
        Q(game_ids__game_id=product.game_id)
        & Q(game_ids__platform=platform_id)
        & Q(developer=True)
    )
    print(product_developer)

    # Creating context for rendering product page
    context = {
        "product": product,
        "product_videos": product_videos,
        "product_screenshots": product_screenshots,
        "product_genres": product_genres,
        "product_cover": product_cover,
        "product_publisher": product_publisher,
        "product_developer": product_developer,
    }
    return render(request, "store_pages/product_page.html", context=context)


# View function for adding products to the cart
def add_to_cart(request):
    # Creating or retrieving the user's cart
    test_cart, created = CurrentCart.objects.get_or_create(owner=request.user)
    add_product = Game.objects.get(id=request.POST["item_id"])
    cover = Cover.objects.get(game_ids=add_product)
    console = Console.objects.get(console_id=add_product.platform)

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
            cart_item_test["item_quantity"] = (
                cart_item_test["item_quantity"] + 1
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


# View function for changing user account details
def change_details(request):
    if request.user.is_authenticated:
        emailform = AddEmailForm()  # Create form for adding email
        passwordform = (
            ChangePasswordForm()
        )  # Create form for changing password
        context = {
            "email_form": emailform,
            "password_change_form": passwordform,
            "emailaddresses": list(
                EmailAddress.objects.filter(user=request.user).order_by(
                    "email"
                )
            ),  # Get list of user's email addresses
            "new_emailaddress": EmailAddress.objects.get_new(
                request.user
            ),  # Get new email address
            "current_emailaddress": EmailAddress.objects.get_verified(
                request.user
            ),  # Get verified email address
        }
        return render(request, "account/change_details.html", context=context)


# View function for removing an item from the cart
def remove_from_cart(request):
    remove_item = request.POST["cart_item_id"]
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
        update_item = request.POST["cart_item_id"]
        get_user_cart = CurrentCart.objects.get(owner=request.user)
        get_item_stock = Game.objects.get(id=request.POST["cart_item_id"])
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


# Set up Mailchimp client using API key and region
mailchimp = Client()
mailchimp.set_config(
    {
        "api_key": settings.MAILCHIMP_API_KEY,
        "server": settings.MAILCHIMP_REGION,
    }
)


# View function for subscribing to a mailing list
def subscribe_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        print(form)
        if form.is_valid():
            try:
                form_email = form.cleaned_data["email"]
                member_info = {
                    "email_address": form_email,
                    "status": "pending",
                }
                response = mailchimp.lists.add_list_member(
                    settings.MAILCHIMP_AUDIENCE_ID,
                    member_info,
                )
                logger.info(f"API call successful: {response}")
                messages.add_message(
                    request,
                    messages.INFO,
                    "Your email address has been submitted."
                    " Please verify via the link sent to "
                    + form_email,
                )
                return HttpResponseRedirect(request.META["HTTP_REFERER"])

            except ApiClientError as error:
                logger.error(f"An exception occurred: {error.text}")
                return HttpResponseRedirect(request.META["HTTP_REFERER"])

    return HttpResponseRedirect(request.META["HTTP_REFERER"])


# View function for displaying user's order history
def my_orders(request):
    if request.user.is_authenticated:
        my_order_list = Orders.objects.filter(owner_id=request.user)

    context = {"my_orders": my_order_list}

    return render(request, "store_pages/my_orders.html", context=context)
