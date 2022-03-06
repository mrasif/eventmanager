from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

User = get_user_model()

class RegisterAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',password='12345678', first_name='Test', last_name='User')

    def test_register_success(self):
        url = '/users/register'
        data = {
            'username': 'testuser1',
            'password': '12345678',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data['token'])

    def test_register_duplicate_username_should_fail(self):
        url = '/users/register'
        data = {
            'username': 'testuser',
            'password': '12345678',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)