from rest_framework import serializers

from products.models import Product
from users.serializers import UserSerializer


class ProductGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["description", "price", "quantity", "is_active", "seller"]
        read_only_fields = [
            "description",
            "price",
            "quantity",
            "is_active",
            "seller",
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    seller = UserSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "description",
            "seller",
            "price",
            "quantity",
            "is_active",
        ]
        read_only_fields = [
            "id",
            "is_active",
            "seller",
        ]
        depth = 1
