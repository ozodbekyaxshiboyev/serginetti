from django.db.models import Sum
from rest_framework import serializers
from django.db import transaction
from account.serializers import UserSerializer
from product.models import ProductSize, Product
from product.serializers import ProductForOrderWishlistSerializer
from .models import (
    Order, OrderItem, OrderItemSize,
    Wishlist, WishlistSize
)


#korzina
class WishlistSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistSize
        fields = ('id','wishlist','productsize','count',)


class WishlistSizeCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistSize
        fields = ('productsize','count',)


class WishlistSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        wishlist_sizes = self.context.get('wishlist_sizes')
        size_serializer = WishlistSizeCheckSerializer(data=wishlist_sizes, many=True)
        size_serializer.is_valid(raise_exception=True)
        return attrs


    def create(self, validated_data):
        wishlist_sizes = self.context['wishlist_sizes']
        with transaction.atomic():
            wishlist = self.Meta.model.objects.create(**validated_data)
            for size in wishlist_sizes:
                productsize = ProductSize.objects.get(id=size.get('productsize'))
                WishlistSize.objects.create(wishlist=wishlist,
                                             productsize=productsize,
                                            count=size.get('count'))

        return wishlist

    class Meta:
        model = Wishlist
        fields = (
            'id',
            'client',
            'product',
            'price',
        )


class WishlistWatchSerializer(serializers.ModelSerializer):
    product = ProductForOrderWishlistSerializer()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        product_sizes = instance.wishlistsize.all()
        image_serializer = WishlistSizeCheckSerializer(product_sizes, many=True)
        representation['sizes'] = image_serializer.data
        representation['total_count'] = instance.get_total_count
        representation['total_price'] = instance.get_total_price
        return representation


    class Meta:
        model = Wishlist
        fields = (
            'id',
            'client',
            'product',
            'price',
        )


class WishlistCheckSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        wishlist_sizes = self.context.get('wishlist_sizes')
        size_serializer = WishlistSizeCheckSerializer(data=wishlist_sizes, many=True)
        size_serializer.is_valid(raise_exception=True)

        wishlist = Wishlist.objects.get(pk=self.context.get('wishlist'))
        with transaction.atomic():
            for wishlistsize in wishlist.wishlistsize.all():
                wishlistsize.delete()

            for size in wishlist_sizes:
                productsize = ProductSize.objects.get(id=size.get('productsize'))
                WishlistSize.objects.create(wishlist=wishlist,
                                             productsize=productsize,
                                            count=size.get('count'))
        return attrs


    class Meta:
        model = Wishlist
        fields = (
            'id',
            'client',
            'product',
            'price',
        )


#ForOrderDetail
class OrderItemForOrderSerializer(serializers.ModelSerializer):
    product = ProductForOrderWishlistSerializer()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        product_sizes = instance.orderitemsize.all()
        size_serializer = OrderItemSizeCheckSerializer(product_sizes, many=True)
        representation['sizes'] = size_serializer.data
        return representation

    class Meta:
        model = OrderItem
        fields = ('id','product','price','get_total_price','get_total_count')


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id','order','product','price',)


class OrderItemCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('product','price',)


class OrderItemSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItemSize
        fields = ('id','orderitem','productsize','count',)


class OrderItemSizeCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItemSize
        fields = ('productsize','count',)


class OrderSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        products = self.context.get('products')
        products_serializer = OrderItemCheckSerializer(data=products, many=True)
        products_serializer.is_valid(raise_exception=True)
        for size in self.context.get('products'):
            size = size.get('sizes')
            sizes_serializer = OrderItemSizeCheckSerializer(data=size, many=True)
            sizes_serializer.is_valid(raise_exception=True)

        return attrs

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        products = instance.orderitem.all()
        orderitem_serializer = OrderItemForOrderSerializer(products, many=True)
        representation['products'] = orderitem_serializer.data
        representation['total_count'] = instance.get_total_count
        representation['total_price'] = instance.get_total_price
        return representation


    def create(self, validated_data):
        products = self.context['products']
        with transaction.atomic():
            order = self.Meta.model.objects.create(**validated_data)
            for size in products:
                product = Product.objects.get(id=size.get('product'))
                orderitem = OrderItem.objects.create(order=order,
                                             product=product,
                                            price=size.get('price'))
                sizes = size.get('sizes')
                for sz in sizes:
                    productsize = ProductSize.objects.get(id=sz.get('productsize'))
                    OrderItemSize.objects.create(orderitem=orderitem,
                                                productsize=productsize,
                                                count=sz.get('count'))
        return order


    class Meta:
        model = Order
        fields = (
            'id',
            'client',
        )



class OrderGETSerializer(serializers.ModelSerializer):
    client = UserSerializer()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        products = instance.orderitem.all()
        orderitem_serializer = OrderItemForOrderSerializer(products, many=True)
        representation['products'] = orderitem_serializer.data
        representation['total_count'] = instance.get_total_count
        representation['total_price'] = instance.get_total_price
        return representation

    class Meta:
        model = Order
        fields = (
            'id',
            'client',
            'code',
            'status',
            'is_paid',
            'created',
        )


class OrderChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'status',
        )

class OrderMySerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['total_count'] = instance.get_total_count
        representation['total_price'] = instance.get_total_price
        return representation

    class Meta:
        model = Order
        fields = (
            'id',
            'client',
            'code',
            'status',
            'created',
        )
