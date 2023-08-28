from django import template
from store_pages.models import *
from store_pages.forms import SignUpForm
from django.contrib.messages import get_messages
from django.db.models import Q



register = template.Library()

@register.simple_tag
def get_consoles():
    all_consoles = Console.objects.all()
    return all_consoles