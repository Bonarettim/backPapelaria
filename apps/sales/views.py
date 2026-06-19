from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import viewsets, status, filters

from .models import Sale
from .serializers import SaleSerializer
from apps.sellers.services.seller_report_service import SellerReportService


class SalePagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 100


class SaleViewSet(viewsets.ModelViewSet):
    queryset = (
        Sale.objects.all()
        .select_related("customer", "seller")
        .prefetch_related("items", "items__product")
        .order_by("-created_at")
    )

    serializer_class = SaleSerializer
    pagination_class = SalePagination

    filter_backends = [filters.SearchFilter]
    search_fields = [
        "customer__name",
        "seller__name",
        "items__product__description",
    ]

    serializer_class = SaleSerializer
    pagination_class = SalePagination

    @action(detail=False, methods=["get"], url_path="commissions-report")
    def commissions_report(self, request):
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        if not start_date or not end_date:
            return Response(
                {"error": "Os parâmetros 'start_date' e 'end_date' são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            report_data = SellerReportService.get_commissions_report(start_date, end_date)
            return Response(report_data, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception:
            return Response({"error": "Erro interno no servidor."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)