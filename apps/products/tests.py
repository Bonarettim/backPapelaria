from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Product


class ProductAPITests(APITestCase):  # Nome corrigido para refletir Produtos
    def setUp(self):
        # Cria um produto de teste no banco em memória antes de rodar os testes
        self.product = Product.objects.create(
            code="000001",
            description="Lapis",
            unit_price="10.00",
            commission_percentage="3.00",
        )
        # Caminho da URL da API de listagem de produtos
        self.url = reverse("product-list")

    def test_list_products_success(self):  # Nome corrigido
        """Garante que a rota GET retorna a lista de produtos com sucesso"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["code"], "000001")

    def test_create_product_invalid_data(self):  # Nome corrigido
        """Garante que a API barra a criação de produto se o código estiver vazio"""
        payload = {
            "code": "",  # Código vazio para forçar o erro de validação
            "description": "Caneta Azul",
            "unit_price": "10.00",
            "commission_percentage": "3.00",
        }
        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
