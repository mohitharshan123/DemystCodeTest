from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Business(models.Model):
    name = models.CharField(max_length=100)
    year_established = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class BalanceSheet(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)])
    profit_or_loss = models.DecimalField(max_digits=10, decimal_places=2)
    assets_value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.business.name} - Year {self.year}"



