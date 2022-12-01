from django.shortcuts import render
from rest_framework import viewsets, status, permissions


from .models import Discount, DiscountItem
from .serializers import DiscountSerializer, DiscountItemSerializer


class DiscountViewset(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer


class DiscountItemViewset(viewsets.ModelViewSet):
    queryset = DiscountItem.objects.all()
    serializer_class = DiscountItemSerializer

