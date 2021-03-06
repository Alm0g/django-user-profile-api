import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status


class RegistrationTestCase(APITestCase):
    def test_registration(self):
        data = {
            "username": "testcase",
            "email": "test@localhost.app",
            "password1": "some_strong_psw",
            "password2": "some_strong_psw"
        }

        response = self.client.post("/api/rest-auth/registration/", data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ProfileViewSetCase(APITestCase):

    list_url = reverse("profile-list")

    def setUp(self):
        self._test_user_name = "davinci"
        self.user = User.objects.create_user(
            username=self._test_user_name,
            password="some-string-psw"
        )
        self.token = Token.objects.create(user=self.user)
        self._api_authentication()

    def _api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

    def test_profile_list_authenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_list_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_profile_detail_retrieve(self):
        response = self.client.get(reverse('profile-detail', kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"], self._test_user_name)

    def test_profile_update_by_owner(self):
        response = self.client.put(
            reverse('profile-detail', kwargs={"pk": 1}),
            {
                "city": "Anchiano",
                "bio": "Renaissance"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            {
                "id": 1, "user": "davinci", "city": "Anchiano",
                "bio": "Renaissance", "avatar": None
            }
        )

    def test_profile_update_by_random_user(self):
        random_user = User.objects.create_user(username="random", password="psw123132")
        self.client.force_authenticate(user=random_user)
        response = self.client.put(
            reverse('profile-detail', kwargs={"pk": 1}),
            {"bio": "HACKED!"}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)