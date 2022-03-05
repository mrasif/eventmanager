from django.contrib import admin
from django.urls import path
from .views import CreateEventAPIView, EventRetriveUpdateDestroyAPIView

app_name = "events"

urlpatterns = [
    path('', CreateEventAPIView.as_view(), name="create_event"),
    path('<int:pk>', EventRetriveUpdateDestroyAPIView.as_view(), name="event_retrieve_update_destroy"),
]