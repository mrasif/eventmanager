from rest_framework import serializers
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
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at','attendees', 'created_by')

class EventUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at','attendees', 'created_by')