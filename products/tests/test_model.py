from products.models import Product
from django.test import TestCase

from users.models import User


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data1 = {
            "username": "gabriel",
            "password": "1234",
            "first_name": "gabriel",
            "last_name": "luz",
            "is_seller": True,
        }

        cls.user_data2 = {
            "username": "eliana",
            "password": "1234",
            "first_name": "eliana",
            "last_name": "luz",
            "is_seller": True,
        }

        cls.product_data = {
            "description": "Smartband XYZ 3.0",
            "price": 100.99,
            "quantity": 15,
        }

        cls.user1 = User(**cls.user_data1)
        cls.user2 = User(**cls.user_data2)
        cls.user1.save()
        cls.user2.save()

        cls.product = Product.objects.create(
            **cls.product_data,
            seller=cls.user1,
        )

    def test_price_max_digits(self):
        max_digits = self.product._meta.get_field("price").max_digits

        self.assertEqual(max_digits, 10)

    def test_price_decimal_places(self):
        decimal_places = self.product._meta.get_field("price").decimal_places

        self.assertEqual(decimal_places, 2)

    def test_if_is_active_is_nullable(self):
        nullable = self.product._meta.get_field("is_active").null

        self.assertTrue(nullable)

    def test_is_active_default(self):
        default = self.product._meta.get_field("is_active").default

        self.assertTrue(default)

    def test_product_fields(self):
        self.assertEqual(
            self.product.description,
            self.product_data["description"],
        )
        self.assertEqual(
            self.product.price,
            self.product_data["price"],
        )
        self.assertEqual(
            self.product.quantity,
            self.product_data["quantity"],
        )

    def test_product_cannot_belong_to_more_than_one_seller(self):

        self.product.seller = self.user2
        self.product.save()

        self.assertNotIn(self.product, self.user1.products.all())
        self.assertIn(self.product, self.user2.products.all())
