from rest_framework import viewsets, status, permissions, generics
from rest_framework.response import Response
from rest_framework.decorators import action

from product.enums import OrderStatus
from .models import (
    Order, OrderItem, OrderItemSize,
    Wishlist, WishlistSize
)
from .permissions import IsNotClient, IsClient
from .serializers import (
    WishlistSerializer, WishlistCheckSerializer, WishlistSizeSerializer,
    OrderSerializer, OrderItemSerializer, OrderItemSizeSerializer, OrderGETSerializer, WishlistWatchSerializer,
    OrderMySerializer, OrderChangeSerializer
)


class WishlistViewset(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated,IsClient]
    http_method_names = ['post','get','delete']


    def get_serializer_class(self):
        serializer_dict = {
            'list': WishlistWatchSerializer,
            'create': WishlistSerializer,
            'retrieve': WishlistWatchSerializer,
        }
        return serializer_dict.get(self.action, self.serializer_class)

    #For update wishlist
    @action(detail=True, methods=['post'], url_path='updatewishlist')
    def updatewishlist(self, request, *args, **kwargs):
        wishlist_sizes = request.data.get('sizes')
        data = request.data
        wishlist = self.get_object()
        serializer = WishlistCheckSerializer(instance=wishlist,data=data, context={'wishlist_sizes': wishlist_sizes,'wishlist':wishlist.id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        wishlist_sizes = request.data.get('sizes')
        data = request.data
        data['client'] = self.request.user.id
        serializer = self.serializer_class(data=data, context={'wishlist_sizes': wishlist_sizes})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    #todo shu kabi junatiladi ikkalasiga ham
    # {
    #     "product": 1,
    #     "price": 6000,
    #     "sizes": [
    #         {"productsize": 1,
    #          "count": 40
    #          },
    #         {"productsize": 2,
    #          "count": 60
    #          }
    #     ]
    #
    # # }


class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated,IsClient]
    http_method_names = ['post','get','delete']


    #For update order
    @action(detail=True, methods=['post'], url_path='updateorder')
    def updateorder(self, request, *args, **kwargs):
        wishlist_sizes = request.data.get('sizes')
        data = request.data
        wishlist = self.get_object()
        serializer = WishlistCheckSerializer(instance=wishlist,data=data, context={'wishlist_sizes': wishlist_sizes,'wishlist':wishlist.id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # For change status order
    @action(detail=True, methods=['post'], url_path='changestatus',permission_classes=[IsNotClient, permissions.IsAuthenticated])
    def changestatus(self, request, *args, **kwargs):
        order = self.get_object()
        status = self.request.data.get('status')

        if status not in [i[0] for i in list(OrderStatus.choices())]:
            return Response({"Xatolik!":"Status xato kiritildi"}, status=status.HTTP_400_BAD_REQUEST)

        order.status = status
        order.save()
        order_serilizer = OrderGETSerializer(order)
        return Response(order_serilizer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        products = request.data.get('products')
        data = request.data
        data['client'] = self.request.user.id
        serializer = self.serializer_class(data=data, context={'products': products})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get_serializer_class(self):
        serializer_dict = {
            'list': OrderMySerializer,
            'create': OrderSerializer,
            'retrieve': OrderGETSerializer,

        }
        return serializer_dict.get(self.action, self.serializer_class)

    #todo shu holatda junatiladi
    # {
    #     "products": [
    #         {"product": 1,
    #          "price": 2000,
    #          "sizes": [
    #              {"productsize": 1,
    #               "count": 50
    #               },
    #              {"productsize": 2,
    #               "count": 70
    #               }
    #             ]
    #          },
    #
    #         {"product": 2,
    #          "price": 3000,
    #          "sizes": [
    #              {"productsize": 1,
    #               "count": 50
    #               },
    #              {"productsize": 2,
    #               "count": 70
    #               }
    #          ]
    #          }
    #
    #     ]
    #
    # }
