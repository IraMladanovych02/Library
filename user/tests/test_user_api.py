from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model


class JWTAuthenticationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse("user:create")
        self.token_url = reverse("user:token_obtain_pair")
        self.refresh_token_url = reverse("user:token_refresh")
        self.verify_token_url = reverse("user:token_verify")
        self.me_url = reverse("user:manage")

        self.user_data = {
            "email": "test@example.com",
            "password": "testpassword",
        }

        self.user = get_user_model().objects.create_user(**self.user_data)

    def get_user_token(self):
        response = self.client.post(
            self.token_url,
            {"email": self.user_data["email"],
             "password": self.user_data["password"]},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data["access"]

    def test_user_can_not_register_without_email(self):
        data = {
            "username": "testname",
            "password": "newpassword"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_login_with_wrong_credentials(self):
        data = {
            "email": "email",
            "password": "newpassword"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_register_with_email(self):
        data = {
            "email": "newuser@example.com",
            "password": "newpassword",
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_can_login_and_get_token(self):
        response = self.client.post(
            self.token_url,
            {"email": self.user_data["email"],
             "password": self.user_data["password"]},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_user_can_refresh_token(self):
        tokens_data = self.client.post(
            self.token_url,
            {"email": self.user_data["email"],
             "password": self.user_data["password"]},
        )
        response = self.client.post(
            self.refresh_token_url,
            {"refresh": tokens_data.data["refresh"]}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_user_can_verify_token(self):
        verify_data = {
            "token": self.get_user_token(),
        }
        response = self.client.post(self.verify_token_url, verify_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_access_protected_endpoint(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.get_user_token()}"
        )
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user_data["email"])
