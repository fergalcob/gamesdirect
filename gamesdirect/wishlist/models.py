from django.db import models
from django.contrib.auth.models import User
from store_pages.models import Game

# Create your models here.

class Wishlist(models.Model):
	wishlist_items = models.ManyToManyField(Game)
	owner = models.ForeignKey(User,on_delete=models.CASCADE)

	def __str__(self):
		return f'Wishlist Owner: {self.owner.username}'
