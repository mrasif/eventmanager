from django.contrib import admin
from django.urls import path
from .views import CreateEventAPIView

app_name = "events"

urlpatterns = [
    path('', CreateEventAPIView.as_view(), name="create_event"),
]