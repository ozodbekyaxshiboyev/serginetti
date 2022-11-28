from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DiscountViewset

router = DefaultRouter()
router.register('discount', DiscountViewset, 'discount')


urlpatterns = [
    path('', include(router.urls)),

]
