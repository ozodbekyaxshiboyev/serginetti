from django.core.validators import MinValueValidator
from django.db import models
import uuid

from account.models import Client
from product.enums import OrderStatus
from product.models import ProductSize, Product, Size


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE,related_name='order')
    code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    status = models.CharField(max_length=20, choices=OrderStatus.choices(), default=OrderStatus.wait_pay.value)
    total_price = models.FloatField(validators=[MinValueValidator(0)],blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def get_total_price(self):
        return sum(item.get_total_price for item in self.orderitem.all())

    @property
    def get_total_count(self):
        return sum(item.get_total_count for item in self.orderitem.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitem')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='orderitem')
    price = models.FloatField(validators=[MinValueValidator(0)])
    total_price = models.FloatField(validators=[MinValueValidator(0)],blank=True, null=True)

    @property
    def get_total_price(self):
        return sum(item.count * self.price for item in self.orderitemsize.all())

    @property
    def get_total_count(self):
        return sum(item.count for item in self.orderitemsize.all())


class OrderItemSize(models.Model):
    orderitem = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='orderitemsize')
    productsize = models.ForeignKey(Size, on_delete=models.PROTECT, related_name='orderitemsize')
    count = models.PositiveIntegerField()





class Wishlist(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE,related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlist')
    price = models.FloatField(validators=[MinValueValidator(0)])
    total_price = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)

    @property
    def get_total_price(self):
        return sum(item.count * self.price for item in self.wishlistsize.all())

    @property
    def get_total_count(self):
        return sum(item.count for item in self.wishlistsize.all())


class WishlistSize(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='wishlistsize')
    productsize = models.ForeignKey(Size, on_delete=models.PROTECT, related_name='wishlistsize')
    count = models.PositiveIntegerField()

