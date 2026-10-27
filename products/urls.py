from django.urls import path

from .views import ProductCreateView, ProductListView


urlpatterns = [
    path("add", ProductCreateView.as_view(), name="product-add"),
    path("list", ProductListView.as_view(), name="product-list"),
]
