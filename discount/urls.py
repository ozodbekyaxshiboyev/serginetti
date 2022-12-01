from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DiscountViewset, DiscountItemViewset

router = DefaultRouter()
router.register('discount', DiscountViewset, 'discount')
router.register('discountitem', DiscountItemViewset, 'discountitem')


urlpatterns = [
    path('', include(router.urls)),

]
