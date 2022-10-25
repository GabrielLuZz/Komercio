from rest_framework import permissions

from users.models import User


class IsSellerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_authenticated and request.user.is_seller:
            return True


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, user: User):
        if "is_active" in request.data:
            return False

        return request.user.is_authenticated and user == request.user
