from django.contrib import admin
from django.urls import path
from .views import LoginApi

app_name = "users"

urlpatterns = [
    path('login', LoginApi.as_view(), name="login"),
]