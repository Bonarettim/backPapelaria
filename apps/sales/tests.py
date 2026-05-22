from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from apps.products.models import Product
from apps.customers.models import Customer
from apps.sellers.models import Seller
from .models import Sale, SaleItem, DayCommissionRule

# Importa a classe SaleService de dentro do seu módulo commission_service
from .services.commission_service import SaleService


class CommissionServiceTestCase(TestCase):
    def setUp(self):
        # Criando dados base para o teste
        self.seller = Seller.objects.create(
            name="Vendedor Teste", email="vendedor@teste.com", phone="11999999999"
        )
        self.customer = Customer.objects.create(
            name="Cliente Teste", email="cliente@teste.com", phone="11888888888"
        )

        # Produto com preço 10.00 e comissão de 8%
        self.product = Product.objects.create(
            code="PRD01",
            description="Caderno",
            unit_price=Decimal("10.00"),
            commission_percentage=Decimal("8.00"),
        )

        # 2026-05-21 cai em uma Quinta-feira (Weekday = 3)
        self.venda_data = timezone.make_aware(timezone.datetime(2026, 5, 21, 12, 0, 0))
        self.sale = Sale.objects.create(
            seller=self.seller,
            customer=self.customer,
            invoice_number="NF-123",
            created_at=self.venda_data,
        )

    def test_calculo_comissao_sem_regra_do_dia(self):
        """Regra 5: Deve aplicar a comissão padrão do produto (8%) se não houver restrição no dia"""
        item = SaleItem(sale=self.sale, product=self.product, quantity=5)

        # Chamada corrigida usando a classe e o método estático:
        SaleService.calculate_and_save_item(item)
        SaleService.recalculate_sale_total(self.sale)

        # Asserts (Validações)
        self.assertEqual(item.unit_price, Decimal("10.00"))
        self.assertEqual(item.subtotal, Decimal("50.00"))  # 5 * 10.00
        self.assertEqual(item.commission_percentage, Decimal("8.00"))
        self.assertEqual(item.commission_amount, Decimal("4.00"))  # 8% de 50.00
        self.assertEqual(self.sale.total_amount, Decimal("50.00"))

    def test_calculo_comissao_respeitando_teto_maximo_do_dia(self):
        """Regra 6: Se o dia limitar a comissão em no máximo 5%, o produto de 8% deve baixar para 5%"""
        # Criando regra para Quinta-feira (dia 3 do weekday) limitado entre 2% e 5%
        DayCommissionRule.objects.create(
            day_of_week=3,
            min_percentage=Decimal("2.00"),
            max_percentage=Decimal("5.00"),
        )

        item = SaleItem(sale=self.sale, product=self.product, quantity=5)

        # Chamada corrigida aqui também:
        SaleService.calculate_and_save_item(item)

        # Asserts (Validações)
        self.assertEqual(
            item.commission_percentage, Decimal("5.00")
        )  # Forçou o teto de 5%
        self.assertEqual(item.commission_amount, Decimal("2.50"))  # 5% de 50.00
