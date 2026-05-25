from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Seller
from .serializers import SellerSerializer
from apps.sellers.services.seller_report_service import SellerReportService


class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer

    @action(detail=False, methods=["get"], url_path="commissions_report")
    def commissions_report(self, request):
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        if not start_date or not end_date:
            return Response(
                {"error": "Os parâmetros 'start_date' e 'end_date' são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            report_data = SellerReportService.get_commissions_report(start_date, end_date)
            return Response(report_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "Erro interno ao gerar relatório."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )