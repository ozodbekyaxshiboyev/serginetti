from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewset,
    ColorViewset,
    SizeViewset,
    CapsuleViewset,
    MadeTypeViewset,
    ProductViewset, ProductImageViewset, ProductSizeViewset, ProductMadeViewset,
    LookbookListCreateAPIView, LookbookDetailAPIView,
    LookbookImageListCreateAPIView, LookbookImageDetailAPIView,
    LookbookVideoListCreateAPIView, LookbookVideoDetailAPIView
)

router = DefaultRouter()
router.register('category', CategoryViewset, 'category')
router.register('color', ColorViewset, 'color')
router.register('size', SizeViewset, 'size')
router.register('capsule', CapsuleViewset, 'capsule')
router.register('madetype', MadeTypeViewset, 'madetype')
router.register('product', ProductViewset, 'product')
router.register('productimage', ProductImageViewset, 'productimage')
router.register('productsize', ProductSizeViewset, 'productsize')
router.register('productmade', ProductMadeViewset, 'productmade')

urlpatterns = [
    path('', include(router.urls)),
    path('lookbook/', LookbookListCreateAPIView.as_view(), name = 'lookbook'),
    path('lookbook/<int:pk>/', LookbookDetailAPIView.as_view(), name = 'lookbook_detail'),
    path('lookbookimage/', LookbookImageListCreateAPIView.as_view(), name = 'lookbookimage'),
    path('lookbookimage/<int:pk>/', LookbookImageDetailAPIView.as_view(), name = 'lookbookimage_detail'),
    path('lookbookvideo/', LookbookVideoListCreateAPIView.as_view(), name = 'lookbookvideo'),
    path('lookbookvideo/<int:pk>/', LookbookVideoDetailAPIView.as_view(), name = 'lookbookvideo_detail'),

]
