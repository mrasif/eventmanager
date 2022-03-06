from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from events.models import Event, Booking

User = get_user_model()

class BookingDetailAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin = User.objects.create_user(
            username = 'admin',
            password = '12345678',
            first_name = 'Admin',
            last_name = 'User',
            is_superuser = True,
        )

        self.user = User.objects.create_user(
            username = 'testuser',
            password = '12345678',
            first_name = 'Test',
            last_name = 'User',
        )

        self.event = Event.objects.create(
            name = 'Test Event 1',
            description = 'Test Description 1',
            location = 'Test Location 1',
            start_date = datetime.now()+timedelta(days=5),
            end_date = datetime.now()+timedelta(days=6),
            booking_start_date = datetime.now()-timedelta(days=1),
            booking_end_date = datetime.now()+timedelta(days=1),
            max_seats = 10,
            created_by = self.admin,
        )

        Booking.objects.create(
            event = self.event,
            user = self.user,
        )

    def test_booking_detail_api_get_success(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get('/events/bookings/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['event']['id'], self.event.id)
        self.assertEqual(response.data['user']['id'], self.user.id)