from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class LoginViewTests(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username='juanp',
            email='juanp@example.com',
            password='Pass12345!'
        )

        self.client = Client()

    def test_login_with_username(self):

        response = self.client.post(
            reverse('login'),
            {
                'username': 'juanp',
                'password': 'Pass12345!',
            }
        )

        self.assertRedirects(response, reverse('home'))

    def test_login_with_email(self):

        response = self.client.post(
            reverse('login'),
            {
                'username': 'juanp@example.com',
                'password': 'Pass12345!',
            }
        )

        self.assertRedirects(response, reverse('home'))

    def test_login_with_wrong_password_shows_error(self):

        response = self.client.post(
            reverse('login'),
            {
                'username': 'juanp',
                'password': 'incorrecta',
            }
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'incorrectos')

    def test_login_with_unknown_email_shows_error_not_crash(self):

        response = self.client.post(
            reverse('login'),
            {
                'username': 'nadie@example.com',
                'password': 'Pass12345!',
            }
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'incorrectos')
