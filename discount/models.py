from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models

from product.enums import DiscountType
from product.models import Product, Category


class Discount(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    percentage = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    from_date = models.DateField(auto_now=True)
    to_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class DiscountItem(models.Model):
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=DiscountType.choices())
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.type == DiscountType.all.value and (self.category or self.product):
            raise ValidationError("Hamma tovar tanlanganda alohida kategory yoki tovar tanlash mumkin emas!")

        if self.type == DiscountType.category.value and self.product or (self.type == DiscountType.category.value and self.category is None):
            raise ValidationError("Kategoryni kiriting product emas!")

        if self.type == DiscountType.product.value and self.category or (self.type == DiscountType.product.value and  self.product is None):
            raise ValidationError("Product kiriting kategory emas!")

    def __str__(self):
        return str(self.discount.name)