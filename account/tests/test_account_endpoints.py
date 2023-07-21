from django.urls import reverse
from faker import Faker
from model_bakery import baker
from rest_framework import status

from account.models import Account
from utils.tests import TestSetup


class AccountTestCase(TestSetup):
    def setUp(self):
        super().setUp()
        self.autheticate()
        self.faker = Faker()

    def test_create_account_with_no_data(self):
        url = reverse("user-list-create")
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_account_with_no_data_user_id(self):
        url = reverse("user-list-create")
        data = {
            "email": "user1@mail.com",
            "username": "user1",
        }
        response = self.client.post(url, data=data)

        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_json["error"], "user_id: This field is required.")

    def test_create_account_with_no_data_email(self):
        url = reverse("user-list-create")
        data = {
            "user_id": 111,
            "username": "user1",
        }
        response = self.client.post(url, data=data)

        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_json["error"], "email: This field is required.")

    def test_create_account_with_no_data_username(self):
        url = reverse("user-list-create")
        data = {
            "user_id": 111,
            "email": "user1@mail.com",
        }
        response = self.client.post(url, data=data)

        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_json["error"], "username: This field is required.")

    def test_create_account_success(self):
        url = reverse("user-list-create")
        data = {
            "user_id": 111,
            "username": "user1",
            "email": "user1@mail.com",
        }
        response = self.client.post(url, data=data)
        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response_json.get("data", None))

    def test_get_list_account_success(self):
        url = reverse("user-list-create")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(response.json()["data"]["results"]), type([]))

    def test_get_list_account_not_empty_success(self):
        for user_id in [111, 112, 113]:
            baker.make(Account, user_id=user_id, status="active")

        url = reverse("user-list-create")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["data"]["results"]), 3)

        # request with pagination
        response = self.client.get(url, {"size": 2, "page": 1})
        response_data = response.json()["data"]

        self.assertEqual(len(response_data["results"]), 2)
        self.assertEqual(response_data["page"], 1)

        # request with pagination page 2
        response = self.client.get(url, {"size": 2, "page": 2})
        response_data = response.json()["data"]

        self.assertEqual(len(response_data["results"]), 1)
        self.assertEqual(response_data["page"], 2)

        # request with username 111
        response = self.client.get(url, {"search": "111"})
        response_data = response.json()["data"]

        self.assertEqual(len(response_data["results"]), 1)
        self.assertEqual(response_data["results"][0]["user_id"], 111)

    def test_get_account_by_user_id_invalid(self):
        account = baker.make(Account, user_id=111, status="active")
        url = reverse("user-detail-suspend-by-id", args=[account.id + 100])

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_account_by_account_id_valid(self):
        account = baker.make(Account, user_id=111, status="active")
        url = reverse("user-detail-suspend-by-id", args=[account.id])

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["data"]["id"], account.id)

    def test_suspend_account_by_account_id_valid(self):
        account = baker.make(Account, user_id=111, status="active")
        url = reverse("user-detail-suspend-by-id", args=[account.id])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_account_by_account_id_invalid(self):
        account = baker.make(Account, user_id=111, status="active")
        url = reverse("user-detail-suspend-by-user_id", args=[account.id + 100])

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_account_by_user_id_valid(self):
        account = baker.make(Account, user_id=111, status="active")
        url = reverse("user-detail-suspend-by-user_id", args=[111])

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["data"]["user_id"], account.user_id)

    def test_suspend_account_by_user_id_valid(self):
        account = baker.make(Account, user_id=111, status="active")
        url = reverse("user-detail-suspend-by-user_id", args=[account.user_id])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
