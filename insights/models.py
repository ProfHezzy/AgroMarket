from django.db import models
from django.conf import settings

class PriceHistory(models.Model):
    """Track product price changes"""
    product = models.ForeignKey('marketplace.Product', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Price Histories"

    def __str__(self):
        return f"{self.product.name} - ${self.price} on {self.recorded_at.date()}"

class MarketTrend(models.Model):
    """Market trend data"""
    category = models.ForeignKey('marketplace.Category', on_delete=models.CASCADE)
    average_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_sales = models.PositiveIntegerField(default=0)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category.name} trend for {self.date}"