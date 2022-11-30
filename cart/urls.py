from django.urls import path

from . import views


urlpatterns = [
    path('cart_api/', views.CartAPI.as_view(), name='cart_api'),
    path('cart_api/<int:id>/', views.CartAPI.as_view(), name='cart_api'),
]