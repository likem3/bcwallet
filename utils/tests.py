from django.contrib.auth.models import User
from merchant.models import Merchant
from model_bakery import baker
from rest_framework.test import APIClient, APITestCase


class TestSetup(APITestCase):
    def setUp(self):
        self.admin_username = "adminr"
        self.admin_password = "passwdr"
        self.admin_email = "adminr@mail.com"
        self.admin = User.objects.create_superuser(
            username=self.admin_username,
            password=self.admin_password,
            email=self.admin_email,
        )

        self.merchant = baker.make(Merchant, status="active")

        return super().setUp()

    def autheticate(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin)

    def tearDown(self):
        return super().tearDown()
