from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Q
from decimal import Decimal
from .models import Sale
from .serializers import SaleSerializer
from apps.sellers.models import Seller


class SaleViewSet(viewsets.ModelViewSet):
    queryset = (
        Sale.objects.all()
        .select_related("customer", "seller")
        .prefetch_related("items", "items__product")
        .order_by("-created_at")
    )

    serializer_class = SaleSerializer

    @action(detail=False, methods=["get"], url_path="commissions-report")
    def commissions_report(self, request):
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        if not start_date or not end_date:
            return Response(
                {
                    "error": "Por favor, forneça start_date e end_date no formato YYYY-MM-DD."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        sellers_with_commissions = Seller.objects.annotate(
            total_comm=Sum(
                "sales__items__commission_amount",
                filter=Q(
                    sales__created_at__date__gte=start_date,
                    sales__created_at__date__lte=end_date,
                ),
            )
        )

        report_data = []
        general_total = Decimal("0.00")

        for seller in sellers_with_commissions:
            total_commission = seller.total_comm or Decimal("0.00")
            general_total += total_commission

            report_data.append(
                {
                    "seller_id": seller.id,
                    "seller_name": seller.name,
                    "total_commission": float(round(total_commission, 2)),
                }
            )

        return Response(
            {
                "period": {"start": start_date, "end": end_date},
                "general_commission_total": float(round(general_total, 2)),
                "sellers": report_data,
            },
            status=status.HTTP_200_OK,
        )
