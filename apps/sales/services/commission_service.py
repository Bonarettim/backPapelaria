# apps/sales/commission_service.py
from decimal import Decimal


class SaleService:
    @staticmethod
    def calculate_and_save_item(sale_item) -> None:

        from apps.sales.models import DayCommissionRule

        product = sale_item.product
        sale_item.unit_price = product.unit_price

        sale_item.subtotal = Decimal(str(sale_item.quantity)) * sale_item.unit_price

        weekday = sale_item.sale.created_at.weekday()
        percentual = product.commission_percentage

        try:
            rule = DayCommissionRule.objects.get(day_of_week=weekday)
            if percentual < rule.min_percentage:
                percentual = rule.min_percentage
            elif percentual > rule.max_percentage:
                percentual = rule.max_percentage
        except DayCommissionRule.DoesNotExist:
            pass

        sale_item.commission_percentage = percentual

        sale_item.commission_amount = sale_item.subtotal * (
            percentual / Decimal("100.00")
        )

        sale_item.save()

    @staticmethod
    def recalculate_sale_total(sale) -> None:
        from django.db.models import Sum

        total = sale.items.aggregate(total_sum=Sum("subtotal"))["total_sum"] or Decimal(
            "0.00"
        )

        sale.total_amount = total
        sale.save(update_fields=["total_amount"])
