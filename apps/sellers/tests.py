from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Seller


class SellerAPITests(APITestCase):
    def setUp(self):
        self.seller = Seller.objects.create(
            name="Matheus", email="matheus@papelaria.com", phone="11999999999"
        )
        self.url = reverse("seller-list")

    def test_list_sellers_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Matheus")

    def test_create_seller_invalid_data(self):
        payload = {"email": "erro@papelaria.com", "phone": "123"}
        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_commissions_report_invalid_params(self):
        url = reverse("seller-commissions-report")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)