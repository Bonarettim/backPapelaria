# Em um arquivo de serviço (ex: apps/sellers/services.py)
from apps.sellers.models import Seller


class SellerReportService:
    @staticmethod
    def get_commissions_report(start_date: str, end_date: str) -> dict:
        from django.db.models import Count, Sum, Q

        sellers_report = Seller.objects.annotate(
            total_vendas=Count(
                "sales",
                filter=Q(sales__created_at__date__range=[start_date, end_date]),
                distinct=True,
            ),
            total_commission=Sum(
                "sales__items__commission_amount",
                filter=Q(sales__created_at__date__range=[start_date, end_date]),
            ),
        )

        vendedores_data = []
        total_commission_period = 0.0

        for seller in sellers_report:
            comissao_vendedor = float(seller.total_commission or 0.0)
            total_commission_period += comissao_vendedor

            vendedores_data.append(
                {
                    "id": str(seller.id).zfill(3),
                    "name": seller.name,
                    "total_vendas": seller.total_vendas,
                    "total_commission": comissao_vendedor,
                }
            )

        return {
            "vendedores": vendedores_data,
            "total_commission_period": total_commission_period,
        }
