from django.urls import path
from .views import register, login, user_products, user_product

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('products/', user_products, name='user_products'),
    path('product/<int:pk>/', user_product, name='user_product'),
]
