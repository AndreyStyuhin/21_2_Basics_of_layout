from django.urls import path
from catalog import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contacts/', views.contacts, name='contacts'),
    path('category/', views.category, name='category'),  # ✅ добавили
    path('orders/', views.orders, name='orders'),        # ✅ добавили
]
