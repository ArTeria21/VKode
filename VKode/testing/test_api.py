from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.test import APIClient

class CustomTokenObtainPairViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.url = reverse('users:token_obtain_pair')
        self.client = APIClient()

    def test_token_obtain_pair(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'password'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_token_obtain_pair_invalid_credentials(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class UserProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = APIClient()
        self.url = reverse('users:user_profile')
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(refresh.access_token))

    def test_user_profile_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_user_profile_unauthenticated(self):
        self.client.credentials()  # Remove the token
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class LoginUserTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.url = reverse('users:login')
        self.client = APIClient()

    def test_login_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_valid_user(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'password'})
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # Redirects after successful login

    def test_login_invalid_user(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Remains on login page
        self.assertContains(response, "Please enter a correct username and password.")

class RegisterUserTest(TestCase):
    def setUp(self):
        self.url = reverse('users:registration')
        self.client = APIClient()

    def test_registration_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_user_registration(self):
        response = self.client.post(self.url, {
            'username': 'newuser',
            'password1': 'nfishnRIJBS_81d_3d1210',
            'password2': 'nfishnRIJBS_81d_3d1210',
            'email': 'newuser@example.com'
        })
        if response.status_code != status.HTTP_302_FOUND:
            print(response.content)  # Print the response content for debugging
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertTrue(User.objects.filter(username='newuser').exists())

class LogoutUserTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.url = reverse('users:logout')
        self.client = APIClient()
        self.client.login(username='testuser', password='password')

    def test_logout_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, reverse('index'))
