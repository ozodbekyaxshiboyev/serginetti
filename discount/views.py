from django.shortcuts import render
from rest_framework import viewsets, status, permissions


from .models import Discount
from .serializers import DiscountSerializer


class DiscountViewset(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer


