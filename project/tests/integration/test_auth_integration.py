from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class TestAuthIntegration(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.register_url = reverse('register')
        self.home_url = reverse('home')

    def test_user_registration_and_login(self):
        # Register
        response = self.client.post(
            self.register_url,
            {
                'username': 'newuser',
                'email': 'newuser@example.com',
                'password1': 'NewUserPass123!',
                'password2': 'NewUserPass123!'
            },
            HTTP_HX_REQUEST='true'  # Simulate HTMX request
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('HX-Redirect', response.headers)
        self.assertEqual(response.headers['HX-Redirect'], self.home_url)

        # Now login with newly created user
        response = self.client.post(
            self.login_url,
            {
                'username': 'newuser',
                'password': 'NewUserPass123!'
            },
            HTTP_HX_REQUEST='true'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('HX-Redirect', response.headers)
        self.assertEqual(response.headers['HX-Redirect'], self.home_url)

        # Verify user is authenticated
        user = User.objects.get(username='newuser')
        self.assertTrue(user.is_authenticated)
