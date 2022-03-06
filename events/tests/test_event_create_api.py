from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from events.models import Event

User = get_user_model()

class EventCreateAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username='admin',
            password='12345678',
            first_name='Admin',
            last_name='User',
            is_superuser=True,
        )

        self.user = User.objects.create_user(
            username='testuser',
            password='12345678',
            first_name='Test',
            last_name='User',
        )

        self.data = {
            'name': 'Test Event 1',
            'description': 'Test Description 1',
            'location': 'Test Location 1',
            'start_date': datetime.now()+timedelta(days=5),
            'end_date': datetime.now()+timedelta(days=6),
            'booking_start_date': datetime.now()+timedelta(days=1),
            'booking_end_date': datetime.now()+timedelta(days=2),
            'max_seats': 10,
        }

    def test_create_event_as_admin_success(self):

        url = '/events/'
        data = self.data

        self.client.force_authenticate(user=self.admin)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'Test Event 1')
        self.assertEqual(response.data['description'], 'Test Description 1')
        self.assertEqual(response.data['location'], 'Test Location 1')
        self.assertEqual(response.data['created_by'], self.admin.id)
        self.assertTrue(response.data['id'])

    def test_create_event_as_user_unsuccessful(self):
        url = '/events/'
        data = self.data

        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 403)