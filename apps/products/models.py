from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Product(models.Model):
    code = models.CharField(max_length=50)

    description = models.CharField(max_length=255)

    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    commission_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )

    def __str__(self):
        return self.description
