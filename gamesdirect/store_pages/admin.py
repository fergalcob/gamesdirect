from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .resource import GameResource  
from .models import  Game, Videos, Screenshots, Cover, Involved_companies, Company, Console, Genres
from wishlist.models import Wishlist
from cart.models import CurrentCart
from orders.models import Orders



# Register your models here.

class GameAdmin(ImportExportModelAdmin):
     resource_class = GameResource  

admin.site.register(Game, GameAdmin)
admin.site.register(Videos)
admin.site.register(Screenshots)
admin.site.register(Cover)
admin.site.register(Involved_companies)
admin.site.register(Company)
admin.site.register(Console)
admin.site.register(Genres)
admin.site.register(Wishlist)
admin.site.register(CurrentCart)
admin.site.register(Orders)