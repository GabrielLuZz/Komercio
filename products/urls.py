from django.urls import path

from . import views as ProductViews

urlpatterns = [
    path(
        "products/",
        ProductViews.ListCreateProductView.as_view(),
    ),
    path(
        "products/<pk>/",
        ProductViews.RetrieveUpdateProductView.as_view(),
    ),
]
