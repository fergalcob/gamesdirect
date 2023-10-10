from django.db import models
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import User


# Create your models here.
	
class CurrentCart(models.Model):
	owner = models.ForeignKey(User,on_delete=models.CASCADE)
	total_price = MoneyField(decimal_places=2, max_digits=6,default=0, default_currency="EUR")
	cart_items = models.JSONField(default=dict)

	def __str__(self):
		return f'Cart Owner: {self.owner.username}'