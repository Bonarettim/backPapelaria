from django.contrib import admin
from .models import DayCommissionRule, Sale, SaleItem


@admin.register(DayCommissionRule)
class DayCommissionRuleAdmin(admin.ModelAdmin):
    list_display = ("get_day_name", "min_percentage", "max_percentage")
    list_editable = ("min_percentage", "max_percentage")

    def get_day_name(self, obj):
        return obj.get_day_of_week_display()

    get_day_name.short_description = "Dia da Semana"


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1
    readonly_fields = (
        "unit_price",
        "subtotal",
        "commission_percentage",
        "commission_amount",
    )


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = (
        "invoice_number",
        "seller",
        "customer",
        "total_amount",
        "created_at",
    )
    search_fields = ("invoice_number", "seller__name", "customer__name")
    list_filter = ("created_at", "seller")
    inlines = [SaleItemInline]
    readonly_fields = ("total_amount",)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.save()
        formset.save_m2m()

        for obj in formset.deleted_objects:
            obj.delete()

        form.instance.update_total_amount()
