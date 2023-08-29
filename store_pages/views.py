import json  
import pytz
import logging
import random
from django.shortcuts import render, redirect
from django.http import JsonResponse
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
from allauth.account.views import  PasswordChangeView, EmailView
from allauth.account.models import EmailAddress
from django.urls import reverse_lazy 
from allauth.utils import get_form_class
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO
import urllib.request
from django.core.paginator import Paginator

import secrets
import string

def index(request):
    on_sale = Game.objects.filter(sale_discount__gte=1).order_by("?")[:8]
    new_releases = Game.objects.filter().order_by("-first_release")[:8]
    top_rated = Game.objects.filter().order_by("-aggregated_rating")[:8]

    context = {
        "on_sale" : on_sale,
        "new_releases" : new_releases,
        "top_rated" : top_rated
    }
    return render(request,"store_pages/index.html", context=context)

def game_addition(data):
    for games in data:
        for platforms in games['game']['platforms']:
            if platforms in [6,130,167,169]:
                new_game,created = Game.objects.get_or_create(game_id = games['game']['id'],platform=platforms)
                if created is True:
                    new_game.game_id = games['game']['id']
                    new_game.aggregated_rating_count = games['game']['aggregated_rating_count']
                    new_game.platform = platforms
                    new_game.first_release = datetime.fromtimestamp(games['game']['first_release_date'],tz=pytz.UTC)
                    new_game.genres = games['game']['genres']
                    new_game.slug = games['game']['slug']
                    new_game.summary = games['game']['summary']
                    new_game.name = games['game']['name']
                    new_game.aggregated_rating = games['game']['aggregated_rating']
                    new_game.save()

                    new_game_cover, created = Cover.objects.get_or_create(cover_id = games['game']['cover']['id'])
                    if created is True:
                        new_game_cover.url = games['game']['cover']['url']
                        new_game_cover.url_thumbnail = games['game']['cover']['url'].replace("t_original", "t_thumb")
                        new_game_cover.cover_id = games['game']['cover']['id']
                        new_game_cover.save()
                        new_game_cover.game_ids.add(new_game)
                        urllib.request.urlretrieve(
                                new_game_cover.url_thumbnail,
                                str(new_game_cover.cover_id) + "_thumb.png")
                        f = Image.open(
                            str(new_game_cover.cover_id) + "_thumb.png"
                        )
                        upload_file_stream = BytesIO()
                        f.save(upload_file_stream, format="webp")
                        upload_file_stream.seek(0)
                        new_game_cover.cover_thumb_resized = ContentFile(
                            upload_file_stream.getvalue(), "cover_thumb" + str(new_game_cover.cover_id) + ".webp"
                        )
                        f.close()
                        urllib.request.urlretrieve(
                                new_game_cover.url,
                                str(new_game_cover.cover_id) + ".png")
                        f = Image.open(
                                str(new_game_cover.cover_id) + ".png"


                        )
                        upload_file_stream = BytesIO()
                        f.save(upload_file_stream, format="webp")
                        upload_file_stream.seek(0)
                        new_game_cover.cover_large_resized = ContentFile(
                            upload_file_stream.getvalue(), "cover_large" + str(new_game_cover.cover_id) + ".webp"
                        )
                        new_game_cover.cover_mobile_resized = ContentFile(
                            upload_file_stream.getvalue(), "cover_mobile" + str(new_game_cover.cover_id) + ".webp"
                        )
                        f.close()
                        new_game_cover.save()
                    else:       
                        new_game_cover.game_ids.add(new_game)
                    try:
                        for videos in games['game']['videos']:

                            new_game_videos, created = Videos.objects.get_or_create(videos_id = videos['id'])
                            if created is True:
                                new_game_videos.videos_id = videos['id']
                                new_game_videos.video_id = videos['video_id']
                                new_game_videos.save()
                                new_game_videos.game_ids.add(new_game)
                    except KeyError:
                        continue

                    try:
                        for screenshots in games['game']['screenshots']:

                            new_game_screenshots, created = Screenshots.objects.get_or_create(screenshots_id = screenshots['id'])
                            if created is True:
                                new_game_screenshots.screenshots_id = screenshots['id']
                                new_game_screenshots.url = screenshots['url']
                                new_game_screenshots.save()
                                new_game_screenshots.game_ids.add(new_game)
                                urllib.request.urlretrieve(
                                        new_game_screenshots.url,
                                        str(new_game_screenshots.screenshots_id) + ".png")
                                f = Image.open(
                                        str(new_game_screenshots.screenshots_id) + ".png"


                                )
                                upload_file_stream = BytesIO()
                                f.save(upload_file_stream, format="webp")
                                upload_file_stream.seek(0)
                                new_game_screenshots.screen_large_resized = ContentFile(
                                    upload_file_stream.getvalue(), "screen_large" + str(new_game_screenshots.screenshots_id) + ".webp"
                                )
                                new_game_screenshots.screen_mobile_resized = ContentFile(
                                    upload_file_stream.getvalue(), "cover_mobile" + str(new_game_screenshots.screenshots_id) + ".webp"
                                )
                                f.close()
                                new_game_cover.save()    
                            else: 
                                new_game_screenshots.game_ids.add(new_game)
                    except KeyError:
                        continue

                    for involved_companies in games['game']['involved_companies']:

                        for companies in involved_companies:
                            new_game_company,created = Company.objects.get_or_create(company_id = involved_companies['company']['id'])
                            if created is True:
                                new_game_company.company_id = involved_companies['company']['id']
                                new_game_company.name = involved_companies['company']['name']
                                new_game_company.slug = involved_companies['company']['slug']
                                new_game_company.save()

                            new_game_involved_companies = Involved_companies()
                            new_game_involved_companies.involved_companies_id = involved_companies['id']
                            new_game_involved_companies.publisher = involved_companies['publisher']
                            new_game_involved_companies.developer = involved_companies['developer']
                            new_game_involved_companies.company_id = new_game_company
                            new_game_involved_companies.save()
                            new_game_involved_companies.game_ids.add(new_game)
def genre_addition(data):
    for genres in data:
        new_genre,created = Genres.objects.get_or_create(genre_id = genres['id'])
        if created is True:
            new_genre.genre_id = genres['id']
            new_genre.slug = genres['slug']
            new_genre.name = genres['name']
            new_genre.save()

def sale_generation():
    random_games = Game.objects.filter().order_by("?")[:40]
    for each_game in random_games:
        each_game.sale_discount = random.randint(1, 50)
        each_game.save()

def stock_assignment():
    game_keys = Game.objects.filter().order_by("?")[:75]
    for games in game_keys:
        random_amount = random.randint(1,30)
        for keys in range(random_amount):
            order_length = 4
            order_number_generator = ''.join(secrets.choice(string.ascii_uppercase + string.digits)for i in range(order_length))+'-'+''.join(secrets.choice(string.ascii_uppercase + string.digits)for i in range(order_length))+'-'+''.join(secrets.choice(string.ascii_uppercase + string.digits)for i in range(order_length))+'-'+''.join(secrets.choice(string.ascii_uppercase + string.digits)for i in range(order_length))
            games.keys_in_stock.append(order_number_generator)
            games.save()

def games(request):
    genres = Genres.objects.all()
    if 'platform'in request.GET:
        referrer = 'platform'
        chosen_selector = Console.objects.get(slug=request.GET['platform'])
        if 'filter' in request.GET:
            chosen_filter = Genres.objects.get(slug=request.GET['filter'])
            if 'sort' in request.GET:
                chosen_sort = request.GET['sort']
                if 'dir' in request.GET:
                    chosen_dir = request.GET['dir']
                    if chosen_dir == 'desc':
                        chosen_sort = f'-{chosen_sort}'
                    game_list = Game.objects.filter(platform=chosen_selector.console_id).filter(genres__contains=[chosen_filter.genre_id]).order_by(chosen_sort)
        
            else:
                game_list = Game.objects.filter(platform=chosen_selector.console_id).filter(genres__contains=[chosen_filter.genre_id])
        
        else:
            if 'sort' in request.GET:
                chosen_sort = request.GET['sort']
                if 'dir' in request.GET:
                    chosen_dir = request.GET['dir']
                    if chosen_dir == 'desc':
                        chosen_sort = f'-{chosen_sort}'
                    game_list = Game.objects.filter(platform=chosen_selector.console_id).order_by(chosen_sort)

            else:
                game_list = Game.objects.filter(platform=chosen_selector.console_id).prefetch_related('cover_set')
    elif 'genres' in request.GET:
        referrer = 'genres'
        chosen_selector= Genres.objects.get(slug=request.GET['genres'])
        if 'filter' in request.GET:
            chosen_filter = Genres.objects.get(slug=request.GET['filter'])
            if 'sort' in request.GET:
                chosen_sort = request.GET['sort']
                if 'dir' in request.GET:
                    chosen_dir = request.GET['dir']
                    if chosen_dir == 'desc':
                        chosen_sort = f'-{chosen_sort}'
                    game_list = Game.objects.filter(genres__contains=[chosen_selector.genre_id]).filter(genres__contains=[chosen_filter.genre_id]).order_by(chosen_sort)
        
            else:
                game_list = Game.objects.filter(genres__contains=[chosen_selector.genre_id]).filter(genres__contains=[chosen_filter.genre_id])
        
        else:
            if 'sort' in request.GET:
                chosen_sort = request.GET['sort']
                if 'dir' in request.GET:
                    chosen_dir = request.GET['dir']
                    if chosen_dir == 'desc':
                        chosen_sort = f'-{chosen_sort}'
                    game_list = Game.objects.filter(genres__contains=[chosen_selector.genre_id]).order_by(chosen_sort)

            else:
                game_list = Game.objects.filter(genres__contains=[chosen_selector.genre_id])
    elif 'company' in request.GET:
        referrer = 'company'
        chosen_selector = Company.objects.get(slug=request.GET['company'])
        games_from_company = Involved_companies.objects.filter(company_id=chosen_selector)
        company_games_list = []
        for each_game in games_from_company:
            for individual_games in each_game.game_ids.all():
                company_games_list.append(individual_games.game_id)
        if 'filter' in request.GET:
            chosen_filter = Genres.objects.get(slug=request.GET['filter'])
            if 'sort' in request.GET:
                chosen_sort = request.GET['sort']
                if 'dir' in request.GET:
                    chosen_dir = request.GET['dir']
                    if chosen_dir == 'desc':
                        chosen_sort = f'-{chosen_sort}'
                    game_list = Game.objects.filter(game_id__in=company_games_list).filter(genres__contains=[chosen_filter.genre_id]).order_by(chosen_sort)
        
            else:
                game_list = Game.objects.filter(game_id__in=company_games_list).filter(genres__contains=[chosen_filter.genre_id])
        
        else:
            if 'sort' in request.GET:
                chosen_sort = request.GET['sort']
                if 'dir' in request.GET:
                    chosen_dir = request.GET['dir']
                    if chosen_dir == 'desc':
                        chosen_sort = f'-{chosen_sort}'
                    game_list = Game.objects.filter(game_id__in=company_games_list).order_by(chosen_sort)

            else:
                game_list = Game.objects.filter(game_id__in=company_games_list)
    elif request.method == 'POST':
        chosen_selector = 'search'
        referrer = None
        search_query = request.POST['search_query']
        game_list = Game.objects.filter(name__icontains=search_query)

    page_number = request.GET.get("page")
    if page_number == None or page_number == "":
        page_number = 1
    paginator = Paginator(game_list, 16)
    page_obj = paginator.page(page_number)
    context = {
        "page_obj" : page_obj,
        "chosen_selector" : chosen_selector,
        "genres" : genres,
        "referrer" : referrer
    }
    return render(request,"store_pages/platform.html", context = context)

def products(request, pk):
    platform_id=request.GET['platform']
    product = Game.objects.get(Q(slug=pk) & Q(platform=platform_id))
    product_videos = Videos.objects.filter(game_ids__game_id = product.game_id)
    product_screenshots = Screenshots.objects.filter(game_ids__game_id = product.game_id)
    product_cover = Cover.objects.get(Q(game_ids__game_id = product.game_id)& Q(game_ids__platform=platform_id))
    product_genres = Genres.objects.filter(genre_id__in=product.genres)
    product_publisher = Involved_companies.objects.filter(Q(game_ids__game_id = product.game_id) & Q(game_ids__platform=platform_id) & Q(publisher = True))
    product_developer = Involved_companies.objects.filter(Q(game_ids__game_id = product.game_id) & Q(game_ids__platform=platform_id) & Q(developer = True))
    context = {
        'product':product,
        'product_videos' :product_videos,
        'product_screenshots':product_screenshots,
        'product_genres' : product_genres,
        'product_cover' : product_cover,
        'product_publisher' : product_publisher,
        'product_developer' : product_developer
    }
    return render(request,"store_pages/product_page.html", context=context)

def add_to_wishlist(request):
    my_wishlist,created = Wishlist.objects.get_or_create(owner=request.user)
    my_wishlist.save()
    my_wishlist.wishlist_items.add(Game.objects.get(Q(game_id=request.POST['item_id'])& Q(platform=request.POST['platform_id']))) 
    return render(request,"store_pages/index.html")

def remove_from_wishlist(request):
    game_to_remove = Game.objects.get(Q(game_id=request.POST['item_id']) & Q(platform=request.POST['platform_id']))
    my_wishlist = Wishlist.objects.get(owner=request.user)
    my_wishlist.wishlist_items.remove(game_to_remove)
    my_wishlist.save()

    return render(request,"account/my_wishlist.html")

class CustomPasswordChangeView(PasswordChangeView):
    template_name = "account/change_details.html"
    success_url = reverse_lazy('change_details')

    def form_invalid(self, form):
        password_change_form = form
        email_form = AddEmailForm()
        return render(self.request, self.template_name, {'password_change_form': password_change_form, 'email_form': email_form,"emailaddresses": list(EmailAddress.objects.filter(user=self.request.user).order_by("email")), "new_emailaddress": EmailAddress.objects.get_new(self.request.user),"current_emailaddress": EmailAddress.objects.get_verified(self.request.user)})
    
class CustomEmailView(EmailView):
    template_name = 'account/change_details.html'
    success_url = reverse_lazy('change_details')

    def form_invalid(self, form):
        email_form = form
        password_change_form = ChangePasswordForm()
        return render(self.request, self.template_name, {'password_change_form': password_change_form, 'email_form': email_form, "emailaddresses": list(EmailAddress.objects.filter(user=self.request.user).order_by("email")), "new_emailaddress": EmailAddress.objects.get_new(self.request.user),"current_emailaddress": EmailAddress.objects.get_verified(self.request.user)})

def add_to_cart(request):
    test_cart, created = CurrentCart.objects.get_or_create(owner=request.user)
    add_product = Game.objects.get(id=request.POST['item_id'])
    cover = Cover.objects.get(game_ids=add_product)
    console = Console.objects.get(console_id = add_product.platform)
    if created is True:
        test_cart.cart_items={'current_cart':[]}
        cart_items = {
            'item_id' : add_product.id,
            'item_quantity': int(request.POST['quantity']),
            'item_price' : str(add_product.sale_price.amount),
            'item_name' : add_product.name,
            'item_thumbnail' : cover.cover_thumb_resized.url,
            'item_slug' : add_product.slug,
            'item_platform' : add_product.platform,
            'item_console' : console.name
        }
        test_cart.cart_items['current_cart'].append(cart_items)
    else:
        cart_item_test = next((item for item in test_cart.cart_items['current_cart'].copy() if item['item_id'] == add_product.id), None)
        if cart_item_test is not None:
            cart_item_test['item_quantity'] = cart_item_test['item_quantity'] + 1
        else:
            cart_items = {
            'item_id' : add_product.id,
            'item_quantity': int(request.POST['quantity']),
            'item_price' : str(add_product.sale_price.amount),
            'item_name' : add_product.name,
            'item_thumbnail' : cover.url_thumbnail,
            'item_slug' : add_product.slug,
            'item_platform' : add_product.platform,
            'item_console' : console.name
        }
            test_cart.cart_items['current_cart'].append(cart_items)

    test_cart.total_price = calculate_total(test_cart.cart_items['current_cart'])
    test_cart.save()

    return JsonResponse({'current_total_json':list("current_total"), 'current_cart':list("product_list")})

def remove_from_cart(request):
    remove_item = request.POST['cart_item_id']
    get_user_cart = CurrentCart.objects.get(owner=request.user)
    cart_item_confirmation = next((item for item in get_user_cart.cart_items['current_cart'].copy() if item['item_id'] == int(remove_item)), None)
    get_user_cart.cart_items['current_cart'].remove(cart_item_confirmation)
    get_user_cart.total_price = calculate_total(get_user_cart.cart_items['current_cart'])
    get_user_cart.save()
    return JsonResponse({'current_total_json':list("current_total"), 'current_cart':list("product_list")})

def update_cart(request):
    new_quantity = request.POST['item_quantity']
    if int(new_quantity) == 0:
        remove_from_cart(request)
    else:
        update_item = request.POST['cart_item_id']
        get_user_cart = CurrentCart.objects.get(owner=request.user)
        get_item_stock = Game.objects.get(id = request.POST['cart_item_id'])
        cart_item_confirmation = next((item for item in get_user_cart.cart_items['current_cart'].copy() if item['item_id'] == int(update_item)), None)
        if int(new_quantity) <= len(get_item_stock.keys_in_stock):
            cart_item_confirmation['item_quantity'] = new_quantity
        get_user_cart.total_price = calculate_total(get_user_cart.cart_items['current_cart'])
        get_user_cart.save()
    
    return JsonResponse({'current_total_json':list("current_total"), 'current_cart':list("product_list")})

def calculate_total(cart_status):
    price_calculation = 0
    for products in cart_status:
        price_calculation += float(products['item_price']) * float  (products['item_quantity'])
    return price_calculation

def subscribe_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                form_email = form.cleaned_data['email']
                member_info = {
                    'email_address': form_email,
                    'status': 'pending',
                }
                response = mailchimp.lists.add_list_member(
                    settings.MAILCHIMP_AUDIENCE_ID,
                    member_info,
                )
                logger.info(f'API call successful: {response}')
                messages.add_message(request, messages.INFO, "Your email address has been submitted. Please verify via the link sent to " + form_email)
                return HttpResponseRedirect(request.META["HTTP_REFERER"])


            except ApiClientError as error:
                logger.error(f'An exception occurred: {error.text}')
                return HttpResponseRedirect(request.META["HTTP_REFERER"])

    return HttpResponseRedirect(request.META["HTTP_REFERER"])

def change_details(request):
    if request.user.is_authenticated:
        emailform = AddEmailForm()
        passwordform = ChangePasswordForm()
        context = {
            'email_form' : emailform,
            'password_change_form' : passwordform,
            'emailaddresses': list(EmailAddress.objects.filter(user=request.user).order_by("email")),
            'new_emailaddress': EmailAddress.objects.get_new(request.user),
            'current_emailaddress': EmailAddress.objects.get_verified(request.user)
        }
        return render(request,"account/change_details.html", context = context)
    
def my_orders(request):
    if request.user.is_authenticated:
        my_order_list = Orders.objects.filter(owner_id = request.user)
    
    context = {
        'my_orders' : my_order_list
    }

    return render(request,"store_pages/my_orders.html", context = context)