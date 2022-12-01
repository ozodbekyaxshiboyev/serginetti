from django.db.models import Sum
from rest_framework import serializers
from django.db import transaction
from account.serializers import UserSerializer
from product.enums import DiscountType
from product.models import ProductSize, Product
from product.serializers import ProductForOrderWishlistSerializer
from .models import Discount, DiscountItem


#korzina
class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = (  'id',
                    'name',
                    'description',
                    'percentage',
                    'from_date',
                    'to_date',
                    'is_active',
                  )



class DiscountItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountItem
        fields = (  'id',
                    'discount',
                    'type',
                    'category',
                    'product',
                    'is_active',
                    )

    def validate(self, attrs):
        type = attrs.get('type')
        category = attrs.get('category')
        product = attrs.get('product')
        if type == DiscountType.all.value and (category or product):
            raise serializers.ValidationError("Hamma tovar tanlanganda alohida kategory yoki tovar tanlash mumkin emas!")

        if type == DiscountType.category.value and product or (type == DiscountType.category.value and category is None):
            raise serializers.ValidationError("Kategoryni kiriting product emas!")

        if type == DiscountType.product.value and category or (type == DiscountType.product.value and  product is None):
            raise serializers.ValidationError("Product kiriting kategory emas!")

        return attrs
