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
                    print('hello')
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
                        print('https:' + new_game_cover.url_thumbnail)
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
                                print(new_game_screenshots.url)
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