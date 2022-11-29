from django.core.exceptions import ValidationError
from .models import DiscountItem, DiscountType
from product.models import Product


def has_discount(product):
    if not isinstance(product, Product):
        raise ValidationError(f"{product} is not instance of Product model")
    discounts = DiscountItem.objects.filter(discount__is_active=True).order_by('-created_date')
    if discounts:
        for discount in discounts:
            if discount.type == DiscountType.all.value:
                return discount.discount
            if discount.type == DiscountType.category.value and discount.category == product.category:
                return discount.discount
            if discount.type == DiscountType.product.value and discount.product == product:
                return discount.discount
    return None
