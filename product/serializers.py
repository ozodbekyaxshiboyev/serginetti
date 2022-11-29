from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db.models import Sum

from discount.services import has_discount

from .models import (
    Category, Color,
    Capsule,Size,
    MadeType,Product,
    ProductMade,ProductSize,
    ProductImage,
    Lookbook, LookbookImage,
    LookbookVideo
)


class LookbookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lookbook
        fields = ('id', 'name','image')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        lookbook_images = instance.lookbookimage.all()
        image_serializer = LookbookImageSerializer(lookbook_images, many=True)
        lookbook_videos = instance.lookbookvideo.all()
        video_serializer = LookbookVideoSerializer(lookbook_videos, many=True)
        representation['lookbook_images'] = image_serializer.data
        representation['lookbook_videos'] = video_serializer.data
        return representation


class LookbookForProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lookbook
        fields = ('id', 'name',)


class LookbookImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LookbookImage
        fields = ('id', 'lookbook','image')


class LookbookVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LookbookVideo
        fields = ('id', 'lookbook','video')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name','image','is_active')


class CapsuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Capsule
        fields = ('id', 'name','image')


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('id', 'name')


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ('id', 'size')


class MadeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MadeType
        fields = ('id', 'name')


class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = ('id','product', 'size','count',)


class ProductSizeForDetailSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['size'] = instance.size.size
        return representation

    class Meta:
        model = ProductSize
        fields = ('count',)


class ProductMadeSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        sum_amount = self.Meta.model.objects.all().aggregate(Sum('amount')).get('amount__sum')
        if sum_amount + validated_data.get('amount') > 100:
            raise serializers.ValidationError('Mahsulot tarkibi 100 foizdan oshmasligi kerak')
        return self.Meta.model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        sum_amount = self.Meta.model.objects.all().aggregate(Sum('amount')).get('amount__sum')
        if sum_amount - instance.amount + validated_data.get('amount') > 100:
            raise serializers.ValidationError('Mahsulot tarkibi 100 foizdan oshmasligi kerak')
        instance.save()
        return instance

    class Meta:
        model = ProductMade
        fields = ('id','product', 'made','amount',)


class ProductMadeForOrderWishlistSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['made'] = instance.made.name
        return representation

    class Meta:
        model = ProductMade
        fields = ('amount',)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id','product', 'get_image_url','image',)


class ProductListSerializer(serializers.ModelSerializer):
    capsule = CapsuleSerializer()
    category = CategorySerializer()
    color = ColorSerializer()


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        product_images = instance.productimage.all()
        image_serializer = ProductImageSerializer(product_images, many=True)
        product_mades = instance.productmade.all()
        made_serializer = ProductMadeForOrderWishlistSerializer(product_mades, many=True)
        representation['product_images'] = image_serializer.data
        representation['product_mades'] = made_serializer.data
        discount = has_discount(instance)
        print(111, discount)
        if discount:
            representation['has_discount'] = True
            representation['discount_amount'] = discount.percentage
        else:
            representation['has_discount'] = False

        return representation

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'code',
            'slug',
            'description',
            'price',
            'capsule',
            'category',
            'color',

        )


class ProductDetailSerializer(serializers.ModelSerializer):
    capsule = CapsuleSerializer()
    category = CategorySerializer()
    color = ColorSerializer()
    lookbook = LookbookForProductSerializer()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        product_images = instance.productimage.all()
        image_serializer = ProductImageSerializer(product_images, many=True)
        product_sizes = instance.productsize.all()
        size_serializer = ProductSizeForDetailSerializer(product_sizes, many=True)
        product_mades = instance.productmade.all()
        made_serializer = ProductMadeForOrderWishlistSerializer(product_mades, many=True)
        representation['product_images'] = image_serializer.data
        # representation['product_sizes'] = size_serializer.data
        representation['product_mades'] = made_serializer.data
        return representation

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'code',
            'slug',
            'description',
            'price',
            'capsule',
            'category',
            'lookbook',
            'color',
            'sell_type',
            'is_main',
            'is_new',
            'is_cheap',
            'is_xit',
            'is_active',
            'created_at',
            'updated_at',
        )


class ProductCreateSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        if attrs.get('price') <= 0:
            raise ValidationError({'Error':'Mahsulot narxi 0 dan katta bo`lishi kerak!'})
        return attrs

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'code',
            'description',
            'price',
            'capsule',
            'category',
            'lookbook',
            'color',
            'sell_type',
            'is_main',
            'is_new',
            'is_cheap',

            #shu ikklasini birga create qilishni o`ylash kerak
            # 'mades',
            # 'sizes',
        )


class ProductForOrderWishlistSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        product_images = instance.productimage.all()
        image_serializer = ProductImageSerializer(product_images, many=True)
        product_mades = instance.productmade.all()
        made_serializer = ProductMadeForOrderWishlistSerializer(product_mades, many=True)
        representation['color'] = instance.color.name
        representation['product_images'] = image_serializer.data
        representation['product_mades'] = made_serializer.data
        return representation

    class Meta:
        model = Product
        fields = (
            'name',
            'code',
            'description',
        )