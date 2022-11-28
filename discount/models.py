from django.db import models


class Discount(models.Model):
    name = models.CharField(max_length=100)
    percentage = models.PositiveIntegerField(default=10)
    from_date = models.DateField()
    to_date = models.DateField()
    is_active = models.BooleanField(default=True)
