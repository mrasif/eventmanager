from django.db import models

# Create your models here.
class Event(models.Model):
    # Indexing these because of frequent searches
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(max_length=500)
    location = models.CharField(max_length=100)
    # Indexing these because of frequent searches
    start_date = models.DateTimeField(db_index=True)
    end_date = models.DateTimeField()
    # Indexing these because of frequent searches
    booking_start_date = models.DateTimeField(db_index=True)
    booking_end_date = models.DateTimeField(db_index=True)
    max_seats = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    attendees = models.ManyToManyField('users.CustomUser', through='Booking', related_name='booked_events')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def has_expired(self):
        return self.end_date < datetime.now()

    @property
    def has_booking_expired(self):
        return self.booking_end_date < datetime.now()

    @property
    def available_seats(self):
        return self.max_seats - self.attendees.count()
    
    @property
    def is_available(self):
        return self.available_seats and not self.has_expired and not self.has_booking_expired and self.booking_start_date <= datetime.now() and self.is_active
    
class Booking(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} booked {self.event.name}'