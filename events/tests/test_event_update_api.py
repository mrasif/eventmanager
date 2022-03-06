from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from events.models import Event

User = get_user_model()

class EventUpdateAPITestCase(APITestCase):
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

    def test_event_update_as_admin_success(self):
        url = '/events/1'

        self.client.force_authenticate(user=self.admin)
        response = self.client.put(url, {
            'name': 'Test Event 1 Updated',
            'description': 'Test Description 1 Updated',
            'location': 'Test Location 1 Updated',
            'start_date': datetime.now()+timedelta(days=5),
            'end_date': datetime.now()+timedelta(days=6),
            'booking_start_date': datetime.now()+timedelta(days=1),
            'booking_end_date': datetime.now()+timedelta(days=2),
            'max_seats': 10,
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Test Event 1 Updated')

    def test_event_update_as_user_unsuccessful(self):
        url = '/events/1'

        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, {
            'name': 'Test Event 1 Updated',
            'description': 'Test Description 1 Updated',
            'location': 'Test Location 1 Updated',
            'start_date': datetime.now()+timedelta(days=5),
            'end_date': datetime.now()+timedelta(days=6),
            'booking_start_date': datetime.now()+timedelta(days=1),
            'booking_end_date': datetime.now()+timedelta(days=2),
            'max_seats': 10,
        }, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], 'You do not have permission to perform this action.')