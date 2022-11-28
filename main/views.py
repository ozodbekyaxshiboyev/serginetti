from rest_framework.response import Response
from rest_framework.views import APIView
from product.models import Capsule, Category, Product
from product.serializers import CapsuleSerializer, CategorySerializer, ProductListSerializer


class MainAPIView(APIView):
    def get(self, request, *args, **kwargs):
        representation = dict()
        capsules = Capsule.objects.all()[:3]
        capsules_serializer = CapsuleSerializer(capsules, many=True)
        categories = Category.objects.filter(is_active=True)
        categories_serializer = CategorySerializer(categories, many=True)
        new_products = Product.objects.filter(is_new=True)[:4]
        new_serializer = ProductListSerializer(new_products, many=True)
        cheap_products = Product.objects.filter(is_cheap=True)[:4]
        cheap_serializer = ProductListSerializer(cheap_products, many=True)
        representation['capsules'] = capsules_serializer.data
        representation['categories'] = categories_serializer.data
        representation['new_products'] = new_serializer.data
        representation['cheap_products'] = cheap_serializer.data
        return Response(representation)

