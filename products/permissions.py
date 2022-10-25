from rest_framework import permissions

from products.models import Product


class IsSellerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_authenticated and request.user.is_seller:
            return True


class IsOwnerSellerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, product: Product):
        if request.method in permissions.SAFE_METHODS:
            return True

        if (
            request.user.is_authenticated
            and request.user.is_seller
            and product.seller == request.user
        ):
            return True
