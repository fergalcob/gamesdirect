from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from store_pages.models import Game
from store_pages.urls import *

class GameSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        # Return a queryset of items from your model
        return Game.objects.all()
    
    def location(self, obj):
        return f'/products/{obj.slug}?platform={obj.platform}'
        
