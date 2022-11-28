from django.db.models import Sum
from rest_framework import serializers
from django.db import transaction
from account.serializers import UserSerializer
from product.models import ProductSize, Product
from product.serializers import ProductForOrderWishlistSerializer
from .models import Discount


#korzina
class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = (  'id',
                    'name',
                    'percentage',
                    'from_date',
                    'to_date',
                    'is_active',
                  )
