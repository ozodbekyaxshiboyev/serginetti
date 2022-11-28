from django.shortcuts import render
from rest_framework import generics, authentication,viewsets
from rest_framework import filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (
CategorySerializer,
CapsuleSerializer, ColorSerializer,
SizeSerializer, MadeTypeSerializer,
ProductSizeSerializer, ProductMadeSerializer,
ProductImageSerializer, ProductDetailSerializer, ProductListSerializer, ProductCreateSerializer,
LookbookSerializer, LookbookImageSerializer,
LookbookVideoSerializer,

)

from .models import (
    Category, Color,
    Capsule,Size,
    MadeType,Product,
    ProductMade,ProductSize,
    ProductImage,
    Lookbook, LookbookImage, LookbookVideo
)

class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ColorViewset(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer


class SizeViewset(viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer


class CapsuleViewset(viewsets.ModelViewSet):
    queryset = Capsule.objects.all()
    serializer_class = CapsuleSerializer


class MadeTypeViewset(viewsets.ModelViewSet):
    queryset = MadeType.objects.all()
    serializer_class = MadeTypeSerializer


class LookbookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lookbook.objects.all()
    serializer_class = LookbookSerializer


class LookbookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lookbook.objects.all()
    serializer_class = LookbookSerializer
    lookup_field = 'pk'


class LookbookImageListCreateAPIView(generics.ListCreateAPIView):
    queryset = LookbookImage.objects.all()
    serializer_class = LookbookImageSerializer


class LookbookImageDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LookbookImage.objects.all()
    serializer_class = LookbookImageSerializer
    lookup_field = 'pk'


class LookbookVideoListCreateAPIView(generics.ListCreateAPIView):
    queryset = LookbookVideo.objects.all()
    serializer_class = LookbookVideoSerializer


class LookbookVideoDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LookbookVideo.objects.all()
    serializer_class = LookbookVideoSerializer
    lookup_field = 'pk'


class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'color','capsule','lookbook','price','sell_type','is_new','is_cheap','is_xit']
    search_fields = ['name', 'color__name','description']

    def get_serializer_class(self):
        serializer_dict = {
            'list': ProductListSerializer,
            'create': ProductCreateSerializer,
            'retrieve': ProductDetailSerializer,
            'update': ProductCreateSerializer,
        }
        return serializer_dict.get(self.action, self.serializer_class)

    # def get_permissions(self):
    #     if self.action in ['update', 'partial_update', 'destroy', 'create']:
    #         self.permission_classes = [IsAuthenticated]
    #     else:
    #         self.permission_classes = [AllowAny]
    #
    #     return super().get_permissions()


class ProductImageViewset(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


class ProductSizeViewset(viewsets.ModelViewSet):
    queryset = ProductSize.objects.all()
    serializer_class = ProductSizeSerializer


class ProductMadeViewset(viewsets.ModelViewSet):
    queryset = ProductMade.objects.all()
    serializer_class = ProductMadeSerializer