from django.db import models
from django.utils import timezone


class DayCommissionRule(models.Model):
    DAY_CHOICES = [
        (0, "Segunda-feira"),
        (1, "Terça-feira"),
        (2, "Quarta-feira"),
        (3, "Quinta-feira"),
        (4, "Sexta-feira"),
        (5, "Sábado"),
        (6, "Domingo"),
    ]

    day_of_week = models.IntegerField(choices=DAY_CHOICES, unique=True)
    min_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    max_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def clean(self):
        super().clean()
        if self.min_percentage is not None and self.max_percentage is not None:
            if self.min_percentage > self.max_percentage:
                self.min_percentage, self.max_percentage = (
                    self.max_percentage,
                    self.min_percentage,
                )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Sale(models.Model):
    seller = models.ForeignKey(
        "sellers.Seller", on_delete=models.CASCADE, related_name="sales"
    )
    customer = models.ForeignKey(
        "customers.Customer", on_delete=models.CASCADE, related_name="sales"
    )
    invoice_number = models.CharField(max_length=50, unique=True)
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, blank=True
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Sale #{self.invoice_number}"

    def update_total_amount(self):
        total = self.items.aggregate(total_sum=models.Sum("subtotal"))["total_sum"] or 0
        self.total_amount = total
        self.save(update_fields=["total_amount"])


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    subtotal = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    commission_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    commission_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )

    def __str__(self):
        return f"{self.product} - Qty {self.quantity}"

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)
