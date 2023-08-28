from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from djmoney.models.fields import MoneyField
from django_resized import ResizedImageField

class Game(models.Model):
	game_id = models.IntegerField(null=True, blank=True)
	aggregated_rating_count = models.IntegerField(null=True, blank=True)
	platform = models.IntegerField(null=True, blank=True)
	first_release = models.DateField(null=True, blank=True)
	genres = ArrayField(models.IntegerField(null=True, blank=True), null=True, blank=True)
	slug = models.CharField(max_length=100, null=True, blank=True)
	summary = models.TextField(max_length=500, null=True, blank=True)
	name = models.CharField(max_length=100, null=True, blank=True)
	aggregated_rating = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	base_price = MoneyField(decimal_places=2, max_digits=6,default=79.99, default_currency="EUR")
	sale_discount = models.IntegerField(blank=True, default=0)
	sale_price = MoneyField(decimal_places=2, max_digits=6,default=0, default_currency="EUR")
	keys_in_stock = ArrayField(models.TextField(max_length=500,null=True, blank=True), null=True, blank=True, default=list)

	class Meta:
		unique_together = ('game_id','platform')

	def save(self, *args, **kwargs):
		self.sale_price = self.base_price - ((self.base_price*self.sale_discount)/100)
		super(Game, self).save(*args, **kwargs)
		
class Videos(models.Model):
	videos_id = models.IntegerField(primary_key=True)
	video_id = models.CharField(max_length=100, null=True, blank=True)
	game_ids = models.ManyToManyField(Game)
	
class Screenshots(models.Model):
	screenshots_id = models.IntegerField(primary_key=True)
	url = models.CharField(max_length=100)
	url_thumbnail = models.CharField(max_length=100)
	game_ids = models.ManyToManyField(Game)
	screen_large_resized = ResizedImageField(size=[400, 500],quality=90, upload_to='media/', blank=True, null=True)
	screen_thumb_resized = ResizedImageField(size=[150, 150],quality=90, upload_to='media/', blank=True, null=True)
	screen_mobile_resized =  ResizedImageField(size=[150, 200],quality=90, upload_to='media/', blank=True, null=True)
	
class Cover(models.Model):
	cover_id = models.IntegerField(primary_key=True)
	url = models.CharField(max_length=100)
	url_thumbnail = models.CharField(max_length=100, null=True, blank=True)
	game_ids = models.ManyToManyField('Game')
	cover_large_resized = ResizedImageField(size=[400, 500],quality=90, upload_to='media/', blank=True, null=True)
	cover_thumb_resized = ResizedImageField(size=[150, 150],quality=90, upload_to='media/', blank=True, null=True)
	cover_mobile_resized =  ResizedImageField(size=[150, 200],quality=90, upload_to='media/', blank=True, null=True)

class Company(models.Model):
	company_id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=100)
	slug = models.CharField(max_length=100)
	
class Involved_companies(models.Model):
	involved_companies_id = models.IntegerField(primary_key=True)
	publisher = models.BooleanField()
	developer = models.BooleanField()
	game_ids = models.ManyToManyField(Game)
	company_id = models.ForeignKey(Company, on_delete=models.CASCADE)

class Console(models.Model):
	console_id = models.IntegerField(primary_key=True)
	slug = models.CharField(max_length=100)
	name = models.CharField(max_length=100)

class Genres(models.Model):
	genre_id = models.IntegerField(primary_key=True)
	slug = models.CharField(max_length=100)
	name = models.CharField(max_length=100)
	
class Wishlist(models.Model):
	wishlist_items = models.ManyToManyField(Game)
	owner = models.ForeignKey(User,on_delete=models.CASCADE)