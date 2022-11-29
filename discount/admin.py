from django.contrib import admin
from .models import Discount, DiscountItem

admin.site.register((Discount,DiscountItem,))
