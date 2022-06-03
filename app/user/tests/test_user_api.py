"""
Testing user creation
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**kwargs):
    """
    Create and return new user
    :param kwargs:
    :return:
    """
    return get_user_model().objects.create_user(**kwargs)


class PublicUserApiTests(TestCase):
    """
    Test public features of the user API
    """
    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_user_success(self):
        """
        Test creating a user is successful
        :return:
        """
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'testuserpublic'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_email_exists_error(self):
        """
        Test error returned if user created with registered email
        :return:
        """
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'testuserpublic'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """
        Test if short password like less than 5 charecters throws error
        :return:
        """
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'testuserpublic'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """
        Test generate token for valid credentials
        :return:
        """
        user_details = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'testuserpublic'
        }
        create_user(**user_details)
        payload = {
            'email': user_details['email'],
            'password': user_details['password']
        }

        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """
        Tests returns error if wrong credentials used
        :return:
        """
        user_details = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'testuserpublic'
        }
        create_user(**user_details)
        payload = {
            'email': user_details['email'],
            'password': "badpass"
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """
        Tests returns error if blank password used
        :return:
        """
        user_details = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'testuserpublic'
        }
        create_user(**user_details)
        payload = {
            'email': user_details['email'],
            'password': ""
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """
        Test authentication is required for users
        :return:
        """
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTest(TestCase):
    """
    Test API requrests that require authentication
    """
    def setUp(self) -> None:
        self.user = create_user(
            email='test@example.com',
            password='testpass123',
            name='Test Name'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_profile_success(self):
        """
        Test retrieving profile authenticated success
        :return:
        """
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_me_not_allowed(self):
        """
        Test POST not allowed for the me endpoint
        :return:
        """
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def update_user_profile(self):
        """
        Test Updating the user profile for the authenticated user
        :return:
        """
        payload = {'name': 'Updated name', 'password': 'newpassword123'}
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
