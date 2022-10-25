from django.urls import path

from rest_framework.authtoken import views as AuthViews
from . import views as UserViews

urlpatterns = [
    path("login/", AuthViews.obtain_auth_token),
    path("accounts/", UserViews.UserView.as_view()),
    path("accounts/newest/<int:num>/", UserViews.NewestUserView.as_view()),
    path(
        "accounts/<pk>/",
        UserViews.UserUpdateView.as_view(),
    ),
    path(
        "accounts/<pk>/management/",
        UserViews.ActivateOrDesactivateUserView.as_view(),
    ),
]
