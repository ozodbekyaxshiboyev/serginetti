from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MainAPIView


urlpatterns = [
    path('main/', MainAPIView.as_view(), name='main'),

]
