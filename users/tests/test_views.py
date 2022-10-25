# movies/tests.py
import json
from rest_framework.test import APITestCase
from users.models import User
from users.serializers import UserSerializer
from rest_framework.authtoken.models import Token


class UserViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.seller_adm = {
            "username": "raphael",
            "password": "1234",
            "first_name": "raphael",
            "last_name": "luz",
            "is_seller": True,
        }

        cls.seller = {
            "username": "gabriel",
            "password": "1234",
            "first_name": "gabriel",
            "last_name": "luz",
            "is_seller": True,
        }

        cls.seller_login = {
            "username": "gabriel",
            "password": "1234",
        }

        cls.non_seller = {
            "username": "marcos",
            "password": "1234",
            "first_name": "marcos",
            "last_name": "luz",
            "is_seller": False,
        }

        cls.non_seller_login = {
            "username": "marcos",
            "password": "1234",
        }

    def test_can_create_an_seller(self):
        response = self.client.post(
            "/api/accounts/",
            self.seller,
        )

        self.assertEqual(response.status_code, 201)

        self.assertEqual(len(response.data), 8)

        self.assertTrue(response.data["is_seller"])

    def test_can_create_an_non_seller(self):
        response = self.client.post(
            "/api/accounts/",
            self.non_seller,
        )

        self.assertEqual(response.status_code, 201)

        self.assertEqual(len(response.data), 8)

        self.assertFalse(response.data["is_seller"])

    def test_try_create_with_wrong_keys(self):
        response = self.client.post("/api/accounts/", {})

        self.assertEqual(response.status_code, 400)

        self.assertEqual(
            response.data["username"][0],
            "This field is required.",
        )
        self.assertEqual(
            response.data["password"][0],
            "This field is required.",
        )
        self.assertEqual(
            response.data["first_name"][0],
            "This field is required.",
        )
        self.assertEqual(
            response.data["last_name"][0],
            "This field is required.",
        )

    def test_can_login_with_a_seller(self):
        self.client.post("/api/accounts/", self.seller, format="json")

        response = self.client.post("/api/login/", self.seller_login)

        self.assertEqual(response.status_code, 200)

        self.assertIn("token", response.data)

    def test_can_login_with_a_non_seller(self):
        self.client.post("/api/accounts/", self.non_seller, format="json")

        response = self.client.post("/api/login/", self.non_seller_login)

        self.assertEqual(response.status_code, 200)

        self.assertIn("token", response.data)

    def test_update_by_owner(self):
        seller = User.objects.create_user(**self.seller)
        token = Token.objects.create(user=seller)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        response = self.client.patch(
            f"/api/accounts/{seller.id}/",
            {"first_name": "eliana"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["first_name"], "eliana")

    def test_update_by_not_owner(self):
        seller = User.objects.create_user(**self.seller)
        non_seller = User.objects.create_user(**self.non_seller)
        token = Token.objects.create(user=seller)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        response = self.client.patch(
            f"/api/accounts/{non_seller.id}/",
            {"name": "eliana"},
        )

        self.assertEqual(response.status_code, 403)

    def test_update_is_active_with_admin(self):
        adm = User.objects.create_superuser(**self.seller_adm)
        token = Token.objects.create(user=adm)

        user_seller = User.objects.create_user(**self.seller)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        response = self.client.patch(
            f"/api/accounts/{user_seller.id}/management/",
            {"is_active": False},
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data["is_active"])

    def test_update_is_active_with_not_admin(self):
        seller = User.objects.create_user(**self.seller)
        token = Token.objects.create(user=seller)

        user_seller = User.objects.create_user(**self.non_seller)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        response = self.client.patch(
            f"/api/accounts/{user_seller.id}/management/",
            {"is_active": False},
        )

        self.assertEqual(response.status_code, 403)

    def test_list_users(self):
        response = self.client.get("/api/accounts/")

        self.assertEqual(200, response.status_code)
