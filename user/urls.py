from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.Register.as_view(), name='registration'),
    path('loginapi/', views.Login.as_view(), name='loginapi'),
    path('verify_token/<str:token>', views.VerifyToken.as_view(), name='verify_token'),
]
