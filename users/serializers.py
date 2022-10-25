from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_active",
            "is_superuser",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "password": {"write_only": True},
            "is_seller": {"required": True},
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
