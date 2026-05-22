from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Customer


class SellerAPITests(APITestCase):
    def setUp(self):
        self.seller = Customer.objects.create(
            name="Natalia  Almeida", email="natalia@gmail.com", phone="1998273233"
        )
        self.url = reverse("customer-list")

    def test_list_customers_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Natalia  Almeida")

    def test_create_customers_invalid_data(self):
        payload = {"email": "erro@papelaria.com", "phone": "123"}
        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
