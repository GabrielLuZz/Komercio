from users.models import User
from django.test import TestCase


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.user_data = {
            "username": "gabriel",
            "password": "1234",
            "first_name": "gabriel",
            "last_name": "luz",
            "is_seller": True,
        }

        cls.user = User(**cls.user_data)
        cls.user.save()

    def test_first_name_max_length(self):
        max_length = self.user._meta.get_field("first_name").max_length

        self.assertEqual(max_length, 50)

    def test_last_name_max_length(self):
        max_length = self.user._meta.get_field("last_name").max_length

        self.assertEqual(max_length, 50)

    def test_is_seller_default(self):
        default = self.user._meta.get_field("is_seller").default

        self.assertFalse(default)

    def test_user_fields(self):
        self.assertEqual(
            self.user.username,
            self.user_data["username"],
        )
        self.assertEqual(
            self.user.first_name,
            self.user_data["first_name"],
        )
        self.assertEqual(
            self.user.last_name,
            self.user_data["last_name"],
        )
        self.assertEqual(
            self.user.is_seller,
            self.user_data["is_seller"],
        )
