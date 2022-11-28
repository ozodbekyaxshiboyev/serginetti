from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    WishlistViewset,
    OrderViewset
)

router = DefaultRouter()
router.register('wishlist', WishlistViewset, 'wishlist')
router.register('order', OrderViewset, 'order')


urlpatterns = [
    path('', include(router.urls)),

]
