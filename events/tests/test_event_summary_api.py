from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from events.models import Event, Booking

User = get_user_model()

class EventSumarryAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin = User.objects.create_user(
            username = 'admin',
            password = '12345678',
            first_name = 'Admin',
            last_name = 'User',
            is_superuser = True,
        )

        self.user1 = User.objects.create_user(
            username = 'testuser1',
            password = '12345678',
            first_name = 'Test',
            last_name = 'User',
        )

        self.user2 = User.objects.create_user(
            username = 'testuser2',
            password = '12345678',
            first_name = 'Test',
            last_name = 'User',
        )

        self.user3 = User.objects.create_user(
            username = 'testuser3',
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
            booking_start_date = datetime.now()-timedelta(days=3),
            booking_end_date = datetime.now()+timedelta(days=1),
            max_seats = 10,
            created_by = self.admin,
        )

        Booking.objects.create(
            event = self.event,
            user = self.user1,
        )

        Booking.objects.create(
            event = self.event,
            user = self.user2,
        )

        Booking.objects.create(
            event = self.event,
            user = self.user3,
        )


    def test_event_summary_api_success(self):
        """
        Test that the event summary api returns the correct data
        """

        # Get the response
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/events/1/summary')
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['attendees_count'], 3)
        self.assertEqual(response.data['available_seats'], 7)
        self.assertEqual(response.data['max_seats'], 10)
        self.assertEqual(len(response.data['attendees_count_group_by_date']), 1)