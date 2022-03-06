from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

User = get_user_model()

class LoginAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',password='12345678', first_name='Test', last_name='User')

    def test_login_success(self):
        url = '/users/login'
        data = {
            'username': 'testuser',
            'password': '12345678'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Logged in successfully')
        self.assertTrue(response.data['token'])
    
    def test_login_incorrect_password_should_fail(self):
        url = '/users/login'
        data = {
            'username': 'testuser',
            'password': '123456789'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['message'], 'Invalid Credentials')

    def test_login_incorrect_username_should_fail(self):
        url = '/users/login'
        data = {
            'username': 'testuser1',
            'password': '12345678'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['message'], 'Invalid Credentials')