from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import (
    ProductListView,
    ContactView,
    CategoryListView,
    OrdersView,
    ProductDetailView,
    ProductCreateView
)

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('contacts/', ContactView.as_view(), name='contacts'),
    path('category/', CategoryListView.as_view(), name='category'),
    path('orders/', OrdersView.as_view(), name='orders'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
]