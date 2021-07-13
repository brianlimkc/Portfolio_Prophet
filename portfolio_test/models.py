from django.db import models
import uuid

# Create your models here.

class Stock(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )
    name = models.CharField(max_length=100,default="",null=True)
    symbol = models.CharField(max_length=10)
    industry = models.CharField(max_length=50,default="",null=True)
    market_cap = models.DecimalField(default=0.00, decimal_places=2, max_digits=15,null=True)
    current_price = models.DecimalField(default=0.00, decimal_places=2, max_digits=9,null=True)
    volume = models.DecimalField(default=0.00, decimal_places=2, max_digits=15,null=True)
    prev_high = models.DecimalField(default=0.00, decimal_places=2, max_digits=9,null=True)
    prev_low = models.DecimalField(default=0.00, decimal_places=2, max_digits=9,null=True)
    price_change = models.DecimalField(default=0.00, decimal_places=2, max_digits=9,null=True)
    percent_change = models.DecimalField(default=0.00, decimal_places=2, max_digits=15,null=True)
    date_added = models.DateTimeField(auto_now_add=True,null=True)
    date_updated = models.DateTimeField(null=True)
    yhat_30 = models.DecimalField(default=0.00, decimal_places=2, max_digits=9,null=True)
    yhat_30_upper = models.DecimalField(default=0.00, decimal_places=2, max_digits=9,null=True)
    yhat_30_lower = models.DecimalField(default=0.00, decimal_places=2, max_digits=9,null=True)
    yhat_30_advice = models.CharField(max_length=20,default="")
    yhat_180 = models.DecimalField(default=0.00, decimal_places=2, max_digits=9,null=True)
    yhat_180_upper = models.DecimalField(default=0.00, decimal_places=2, max_digits=9,null=True)
    yhat_180_lower = models.DecimalField(default=0.00, decimal_places=2, max_digits=9,null=True)
    yhat_180_advice = models.CharField(max_length=20,default="")
    yhat_365 = models.DecimalField(default=0.00, decimal_places=2, max_digits=9,null=True)
    yhat_365_upper = models.DecimalField(default=0.00, decimal_places=2, max_digits=9,null=True)
    yhat_365_lower = models.DecimalField(default=0.00, decimal_places=2, max_digits=9,null=True)
    yhat_365_advice = models.CharField(max_length=20,default="")

    def __str__(self):
        return self.name

class Historical_Stock_Data(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )

    stock_id = models.ForeignKey(
        Stock, 
        on_delete=models.CASCADE, 
        related_name="stock_forecast_id")

    date_recorded = models.DateTimeField()
    price_open = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    price_close = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    price_high = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    price_low = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    volume = models.DecimalField(default=0.00, decimal_places=2, max_digits=15)


class Forecast_Record(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )
    stock_id = models.ForeignKey(
        Stock, 
        on_delete=models.CASCADE, 
        related_name="stock_data_id")
    date = models.DateTimeField()
    yhat = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    yhat_upper = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    yhat_lower = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    