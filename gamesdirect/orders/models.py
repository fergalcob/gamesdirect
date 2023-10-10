from django.db import models
from django.contrib.auth.models import User
from djmoney.models.fields import MoneyField

# Create your models here.
class Orders(models.Model):
	owner_id = models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True)
	order_number = models.CharField(max_length=24,primary_key=True)
	order_items = models.JSONField(default=dict)
	total_price = MoneyField(decimal_places=2, max_digits=6,default=0, default_currency="EUR")
	order_status = models.CharField(max_length=24,default="Pending Payment")
	order_date = models.DateField(null=True, blank=True)

	def __str__(self):
		return f'Order No.: #{self.order_number}'