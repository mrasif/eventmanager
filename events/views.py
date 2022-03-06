from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from .seializers import EventCreateSerializer, EventListSerializer, EventUpdateSerializer, BookingListSerializer, BookingCreateSerializer, EventSummarySerializer
from .permissions import IsAdminUser
from .models import Event, Booking
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


class EventSummaryAPIView(RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSummarySerializer
    permission_classes = [IsAdminUser,]

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        data = response.data
        obj = self.get_object()
        data['attendees_count_group_by_date']= obj.attendees_count_group_by_date
        response.data= data
        return response

class BookingListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated,]
    # override serializer for different methods
    def get_queryset(self):
        event_id = self.kwargs['pk']
        qs = Booking.objects.filter(event=event_id)
        if self.request.user.is_superuser:
            return qs
        return qs.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BookingCreateSerializer
        return BookingListSerializer