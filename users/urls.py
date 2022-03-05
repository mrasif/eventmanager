from django.contrib import admin
from django.urls import path
from .views import LoginAPIView, RegisterAPIView

app_name = "users"

urlpatterns = [
    path('login', LoginAPIView().as_view(), name="login"),
    path('register', RegisterAPIView().as_view(), name="register"),
]