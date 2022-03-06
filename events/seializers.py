from datetime import datetime
from rest_framework import serializers
from users.serializers import UserPublicSerializer
from .models import Event, Booking

class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at','attendees', 'created_by', 'is_active')

    def validate(self, attrs):
        attrs['created_by'] = self.context['request'].user
        attrs['is_active'] = True
        return attrs

class EventListSerializer(serializers.ModelSerializer):

    created_by = UserPublicSerializer()
    # Removed attendees because it discloses the others users information, and event list is public for all
    # attendees = UserPublicSerializer(many=True)
    is_active = serializers.BooleanField(read_only=True)
    is_available = serializers.BooleanField(read_only=True)
    available_seats = serializers.IntegerField(read_only=True)
    attendees_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Event
        exclude = ('attendees',)
        read_only_fields = ('created_at', 'updated_at', 'attendees', 'created_by')

class EventUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at','attendees', 'created_by')


class BookingCountByDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('created_at', 'attendees_count')
class EventSummarySerializer(serializers.ModelSerializer):

    created_by = UserPublicSerializer()
    is_active = serializers.BooleanField(read_only=True)
    is_available = serializers.BooleanField(read_only=True)
    available_seats = serializers.IntegerField(read_only=True)
    attendees_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Event
        exclude = ('attendees',)
        read_only_fields = ('created_at', 'updated_at', 'attendees', 'created_by')

class EventListPublicSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(read_only=True)
    is_available = serializers.BooleanField(read_only=True)
    available_seats = serializers.IntegerField(read_only=True)
    attendees_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Event
        exclude = ('created_by', 'created_at', 'updated_at', 'attendees')
        read_only_fields = ('created_at', 'updated_at','attendees', 'created_by')

class BookingListSerializer(serializers.ModelSerializer):
    event = EventListPublicSerializer(many=False)
    user = UserPublicSerializer(many=False)
    class Meta:
        model = Booking
        fields = ('id', 'event', 'user', 'created_at', 'updated_at')


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'event', 'user')

    def validate(self, attrs):
        attrs['user'] = self.context['request'].user
        attrs['event'] = Event.objects.get(pk=self.context['view'].kwargs['pk'])

        event = Event.objects.get(pk=self.context['view'].kwargs['pk'])
        if not event.is_active:
            raise serializers.ValidationError("Event is not active")
        if event.has_booking_expired:
            raise serializers.ValidationError("Event has expired")
        if datetime.now() < event.booking_start_date:
            raise serializers.ValidationError("Booking start date has not been reached")
        if not event.is_available:
            raise serializers.ValidationError("Event is not available")
        
        return attrs

    def validate_event(self, value):
        event = Event.objects.get(pk=self.context['view'].kwargs['pk'])
        if not event.is_active:
            raise serializers.ValidationError("Event is not active")
        if event.has_booking_expired:
            raise serializers.ValidationError("Event has expired")
        if datetime.now() < event.booking_start_date:
            raise serializers.ValidationError("Booking start date has not been reached")
        if not event.is_available:
            raise serializers.ValidationError("Event is not available")
        return value

class BookingDetailSerializer(serializers.ModelSerializer):
    event = EventListPublicSerializer(many=False)
    user = UserPublicSerializer(many=False)
    class Meta:
        model = Booking
        fields = ('id', 'event', 'user', 'created_at', 'updated_at')