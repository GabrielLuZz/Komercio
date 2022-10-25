# movies/tests.py
from rest_framework.test import APITestCase
from users.models import User
from users.serializers import UserSerializer
from rest_framework.authtoken.models import Token
from products.models import Product


class ProductViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product1_data = {
            "description": "Smartband XYZ 3.0",
            "price": 100.99,
            "quantity": 15,
        }

        cls.product2_data = {
            "description": "Smartband XYZ 3.0",
            "price": 100.99,
            "quantity": 15,
        }

        cls.base_url = "/api/products/"

        cls.seller_adm_data = {
            "username": "raphael",
            "password": "1234",
            "first_name": "raphael",
            "last_name": "luz",
            "is_seller": True,
        }

        cls.seller_adm_login_data = {
            "username": "raphael",
            "password": "1234",
        }

        cls.seller_data = {
            "username": "gabriel",
            "password": "1234",
            "first_name": "gabriel",
            "last_name": "luz",
            "is_seller": True,
        }

        cls.seller_login_data = {
            "username": "gabriel",
            "password": "1234",
        }

        cls.seller2_data = {
            "username": "victor",
            "password": "1234",
            "first_name": "victor",
            "last_name": "luz",
            "is_seller": True,
        }

        cls.seller2_login_data = {
            "username": "victor",
            "password": "1234",
        }

        cls.non_seller_data = {
            "username": "marcos",
            "password": "1234",
            "first_name": "marcos",
            "last_name": "luz",
            "is_seller": False,
        }

        cls.non_seller_login_data = {
            "username": "marcos",
            "password": "1234",
        }

        cls.seller_adm = User.objects.create_superuser(**cls.seller_adm_data)
        cls.token_adm = Token.objects.create(user=cls.seller_adm)

        cls.seller = User.objects.create_user(**cls.seller_data)
        cls.token_seller = Token.objects.create(user=cls.seller)

        cls.seller2 = User.objects.create_user(**cls.seller2_data)
        cls.token_seller2 = Token.objects.create(user=cls.seller2)

        cls.non_seller = User.objects.create_user(**cls.non_seller_data)
        cls.token_non_seller = Token.objects.create(user=cls.non_seller)

        cls.product_created = Product.objects.create(
            **cls.product2_data,
            seller=cls.seller2,
        )

        cls.products = [
            Product.objects.create(
                description=f"Produto {product_id}",
                price=5,
                quantity=7,
                seller=cls.seller,
            )
            for product_id in range(1, 5)
        ]

    def test_can_create_product_with_seller(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_seller.key,
        )

        response = self.client.post(
            self.base_url,
            self.product1_data,
        )

        self.assertEqual(201, response.status_code)
        self.assertEqual(len(response.data.keys()), 6)

    def test_create_product_without_token(self):
        response = self.client.post(
            self.base_url,
            self.product1_data,
        )

        self.assertEqual(401, response.status_code)
        self.assertEqual(
            response.data["detail"],
            "Authentication credentials were not provided.",
        )

    def test_create_product_with_non_seller(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_non_seller.key,
        )

        response = self.client.post(
            self.base_url,
            self.product1_data,
        )

        self.assertEqual(403, response.status_code)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to perform this action.",
        )

    def test_can_owner_edit_product(self):
        product = Product.objects.create(
            **self.product1_data,
            seller=self.seller,
        )
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_seller.key,
        )

        response = self.client.patch(
            f"{self.base_url}{product.id}/",
            {"price": 90},
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(len(response.data.keys()), 6)

    def test_only_owner_can_edit_product(self):
        product = Product.objects.create(
            **self.product1_data,
            seller=self.seller,
        )
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_seller2.key,
        )

        response = self.client.patch(
            f"{self.base_url}{product.id}/",
            {"price": 110},
        )

        self.assertEqual(response.status_code, 403)

    def test_can_list_products(self):
        response = self.client.get(
            self.base_url,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"][0].keys()), 5)

    def test_can_filter_product(self):
        response = self.client.get(
            f"{self.base_url}{self.product_created.id}/",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.keys()), 6)

    def test_create_with_wrong_keys(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_seller.key,
        )

        response = self.client.post(
            self.base_url,
            {},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["description"][0],
            "This field is required.",
        )
        self.assertEqual(
            response.data["price"][0],
            "This field is required.",
        )
        self.assertEqual(
            response.data["quantity"][0],
            "This field is required.",
        )

    def test_can_create_with_negative_number(self):
        product_data = {
            "description": "microondas",
            "price": 120,
            "quantity": -5,
        }

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_seller2.key,
        )

        response = self.client.post(
            self.base_url,
            product_data,
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "Ensure this value is greater than or equal to 0.",
            response.data["quantity"],
        )
