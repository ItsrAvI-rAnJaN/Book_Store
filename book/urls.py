from django.urls import path
from . import views

urlpatterns = [
    path('bookapi/', views.BookAPI.as_view(), name='bookapi'),

]