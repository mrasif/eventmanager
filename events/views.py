from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .seializers import EventCreateSerializer, EventListSerializer, EventUpdateSerializer
from .permissions import IsAdminUser
from .models import Event
# Create your views here.

class CreateEventAPIView(ListCreateAPIView):
    queryset = Event.objects.all()

    # override serializer for different methods
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EventCreateSerializer
        return EventListSerializer
    
    # override permission for different methods
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser(),]
        return [IsAuthenticated(),]

class EventRetriveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()

    # override serializer for different methods
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return EventUpdateSerializer
        return EventListSerializer
    
    # override permission for different methods
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser(),]
        return [IsAuthenticated(),]