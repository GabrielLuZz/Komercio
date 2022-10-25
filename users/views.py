from rest_framework import views
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from users.models import User
from users.serializers import UserSerializer

from . import permissions
from rest_framework.permissions import IsAdminUser


class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class NewestUserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        num_of_users = self.kwargs["num"]
        return self.queryset.order_by("-date_joined")[0:num_of_users]


class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsOwner]


class ActivateOrDesactivateUserView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
