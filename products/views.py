from rest_framework import generics

from products.models import Product

from . import permissions

from rest_framework.authentication import TokenAuthentication

from . import mixins

from . import serializers


class ListCreateProductView(
    mixins.SerializerByMethodMixin,
    generics.ListCreateAPIView,
):
    queryset = Product.objects.all()
    serializer_map = {
        "GET": serializers.ProductGeneralSerializer,
        "POST": serializers.ProductDetailSerializer,
    }
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsSellerOrReadOnly]


class RetrieveUpdateProductView(
    mixins.SerializerByMethodMixin, generics.RetrieveUpdateAPIView
):
    queryset = Product.objects.all()
    serializer_map = {
        "GET": serializers.ProductDetailSerializer,
        "PATCH": serializers.ProductDetailSerializer,
    }
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsOwnerSellerOrReadOnly]
