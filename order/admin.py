from django.contrib import admin
from .models import Order, OrderItem, OrderItemSize, \
    Wishlist, WishlistSize


admin.site.register((Order, OrderItem, OrderItemSize, Wishlist, WishlistSize,))
