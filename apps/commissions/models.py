from django.db import models


class CommissionRule(models.Model):
    WEEKDAYS = [
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    ]

    weekday = models.IntegerField(choices=WEEKDAYS, unique=True)

    min_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    max_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "commission_rules"

    def __str__(self):
        return self.get_weekday_display()
