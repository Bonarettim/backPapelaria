from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Product


class ProductAPITests(APITestCase):
    def setUp(self):
        self.product = Product.objects.create(
            code="000001",
            description="Lapis",
            unit_price="10.00",
            commission_percentage="3.00",
        )
        self.url = reverse("product-list")

    def test_list_products_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["code"], "000001")

    def test_create_product_invalid_data(self):
        payload = {
            "code": "",
            "description": "Caneta Azul",
            "unit_price": "10.00",
            "commission_percentage": "3.00",
        }
        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
