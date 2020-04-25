from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from oauth2_provider.models import get_application_model, AccessToken

import datetime

from .models import User


class UserManagerTests(APITestCase):

    def setUp(self):
        self.email = 'michael_scofield@gmail.com'
        self.name = 'Michael Scofield'
        self.password = 'Sara'

    def test_create_user(self):
        user = User.objects.create_user(
            email=self.email,
            name=self.name,
            password=self.password
        )
        self.assertEqual(user.email, self.email)
        self.assertEqual(user.name, self.name)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertIsNone(user.username)

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(
            email=self.email,
            name=self.name,
            password=self.password
        )
        self.assertEqual(superuser.email, self.email)
        self.assertEqual(superuser.name, self.name)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertIsNone(superuser.username)


class SignupViewTests(APITestCase):

    def setUp(self):
        self.url = 'http://localhost:8000/signup/'
        self.data = {
            'name': 'Michael Scofield',
            'email': 'ms@gmail.com',
            'password': 'sara1234'
        }

    def test_signup_successful(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().name, self.data['name'])

    def test_signup_invalid_email(self):
        self.data['email'] = 'invalid_email.com'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTests(APITestCase):

    def setUp(self):
        self.url = 'http://localhost:8000/oauth/'
        self.client_id = '1234'
        self.client_secret = '1234'
        self.data = {
            'email': 'ms@gmail.com',
            'password': 'sara1234',
        }
        User.objects.create_user(
            email='ms@gmail.com',
            name='Michael Scofield',
            password='sara1234'
        )

    # def test_login_successful(self):
        # response = self.client.post(self.url, self.data, format='json')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertIsNotNone(response['access_token'])


class HomePageViewTests(APITestCase):

    def setUp(self):
        superuser = User.objects.create_superuser(
            email='ms@gmail.com',
            name='Michael Scofield',
            password='sara1234'
        )

        Application = get_application_model()

        self.application = Application.objects.create(
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
            redirect_uris='',
            name='dummy',
            user=superuser
        )
        self.application.save()

        self.url = 'http://localhost:8000/home/'

    def test_home_page_authorized(self):
        user = User.objects.create_user(
            email='lb@gmail.com',
            name='Lincoln Burrows',
            password='veronica'
        )
        self.access_token = AccessToken.objects.create(
            user=user,
            scope='read write',
            expires=timezone.now() + datetime.timedelta(seconds=300),
            token='secret-access-token-key',
            application=self.application
        )
        response = self.client.get(self.url, format='json',
                                   HTTP_AUTHORIZATION="Bearer {0}"
                                   .format(self.access_token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_home_page_unauthorized(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
