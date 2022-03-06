from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from events.models import Event

User = get_user_model()

class EventBookingCreateAPITestCase(APITestCase):
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

        Event.objects.create(
            name = 'Test Event 1',
            description = 'Test Description 1',
            location = 'Test Location 1',
            start_date = datetime.now()+timedelta(days=5),
            end_date = datetime.now()+timedelta(days=6),
            booking_start_date = datetime.now()+timedelta(days=1),
            booking_end_date = datetime.now()+timedelta(days=2),
            max_seats = 10,
            created_by = self.admin,
        )

        Event.objects.create(
            name = 'Test Event 2',
            description = 'Test Description 2',
            location = 'Test Location 2',
            start_date = datetime.now()+timedelta(days=5),
            end_date = datetime.now()+timedelta(days=6),
            booking_start_date = datetime.now()-timedelta(days=1),
            booking_end_date = datetime.now()+timedelta(days=1),
            max_seats = 10,
            created_by = self.admin,
        )

        Event.objects.create(
            name = 'Test Event 3',
            description = 'Test Description 3',
            location = 'Test Location 3',
            start_date = datetime.now()+timedelta(days=5),
            end_date = datetime.now()+timedelta(days=6),
            booking_start_date = datetime.now()-timedelta(days=2),
            booking_end_date = datetime.now()-timedelta(days=1),
            max_seats = 10,
            created_by = self.admin,
        )
    
    def test_event_booking_create_as_user_success(self):
        url = '/events/2/bookings'
        data = {}

        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_event_booking_create_as_user_before_booking_window_unsuccessful(self):
        url = '/events/1/bookings'
        data = {}

        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_event_booking_create_as_user_after_booking_window_unsuccessful(self):
        url = '/events/3/bookings'
        data = {}

        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)