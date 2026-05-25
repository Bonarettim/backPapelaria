from rest_framework import serializers
from django.db import transaction
from .models import Sale, SaleItem
from apps.customers.serializers import CustomerSerializer
from apps.sellers.serializers import SellerSerializer
from apps.products.serializers import ProductSerializer
from .services.commission_service import SaleService


class SaleItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    product_details = ProductSerializer(source="product", read_only=True)

    class Meta:
        model = SaleItem
        fields = [
            "id",
            "product",
            "product_details",
            "quantity",
            "unit_price",
            "subtotal",
            "commission_percentage",
            "commission_amount",
        ]
        read_only_fields = [
            "unit_price",
            "subtotal",
            "commission_percentage",
            "commission_amount",
        ]


class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True)
    customer_details = CustomerSerializer(source="customer", read_only=True)
    seller_details = SellerSerializer(source="seller", read_only=True)

    class Meta:
        model = Sale
        fields = [
            "id",
            "invoice_number",
            "customer",
            "customer_details",
            "seller",
            "seller_details",
            "total_amount",
            "created_at",
            "items",
        ]
        read_only_fields = ["total_amount", "created_at"]

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop("items")
        sale = Sale.objects.create(**validated_data)

        for item_data in items_data:
            item_data.pop("id", None)
            item = SaleItem(sale=sale, **item_data)
            SaleService.calculate_and_save_item(item)

        SaleService.recalculate_sale_total(sale)
        return sale

    @transaction.atomic
    def update(self, instance, validated_data):
        items_data = validated_data.pop("items", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if items_data is not None:
            existing_items = {item.id: item for item in instance.items.all()}
            keep_item_ids = []

            for item_data in items_data:
                item_id = item_data.get("id")

                if item_id and item_id in existing_items:
                    item = existing_items[item_id]
                    item.product = item_data.get("product", item.product)
                    item.quantity = item_data.get("quantity", item.quantity)
                else:
                    item = SaleItem(sale=instance, **item_data)

                SaleService.calculate_and_save_item(item)
                keep_item_ids.append(item.id)

            for item_id, item in existing_items.items():
                if item_id not in keep_item_ids:
                    item.delete()

        SaleService.recalculate_sale_total(instance)
        return instance
