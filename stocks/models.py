from django.db import models
from accounts.models import *

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
    yhat_30_advice = models.CharField(max_length=20,default="",null=True)
    yhat_180 = models.DecimalField(default=0.00, decimal_places=2, max_digits=9,null=True)
    yhat_180_upper = models.DecimalField(default=0.00, decimal_places=2, max_digits=9,null=True)
    yhat_180_lower = models.DecimalField(default=0.00, decimal_places=2, max_digits=9,null=True)
    yhat_180_advice = models.CharField(max_length=20,default="",null=True)
    yhat_365 = models.DecimalField(default=0.00, decimal_places=2, max_digits=9,null=True)
    yhat_365_upper = models.DecimalField(default=0.00, decimal_places=2, max_digits=9,null=True)
    yhat_365_lower = models.DecimalField(default=0.00, decimal_places=2, max_digits=9,null=True)
    yhat_365_advice = models.CharField(max_length=20,default="",null=True)

    def __str__(self):
        return self.name

    def serialize(self):
        return {
        "id" : self.id,
        "name" : self.name,
        "symbol" : self.symbol,
        "industry" : self.industry,
        "marketCap" : float(self.market_cap),
        "currentPrice" : float(self.current_price),
        "volume" : float(self.volume),
        "high" : float(self.prev_high),
        "low" : float(self.prev_low),
        "price_change" : float(self.price_change),
        "percent_change" : float(self.percent_change),
        "yhat_30" : float(self.yhat_30),
        "yhat_30_upper" : float(self.yhat_30_upper),
        "yhat_30_lower" : float(self.yhat_30_lower),
        "yhat_30_advice" : self.yhat_30_advice,
        "yhat_30_ratio" : float(round(((self.yhat_30 - self.current_price) / self.yhat_30),2)),
        "yhat_180" : float(self.yhat_180),
        "yhat_180_upper" : float(self.yhat_180_upper),
        "yhat_180_lower" : float(self.yhat_180_lower),
        "yhat_180_advice" : self.yhat_180_advice,
        "yhat_180_ratio" : float(round(((self.yhat_180 - self.current_price) / self.yhat_180),2)),
        "yhat_365" : float(self.yhat_365),
        "yhat_365_upper" : float(self.yhat_365_upper),
        "yhat_365_lower" : float(self.yhat_365_lower),
        "yhat_365_advice" : self.yhat_365_advice,
        "yhat_365_ratio" : float(round(((self.yhat_365 - self.current_price) / self.yhat_365),2)),
        }
class Watchlist(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )

    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="watchlist_user")

    stock_id = models.ForeignKey(
        Stock,
        on_delete=models.CASCADE,
        related_name="watchlist_stock")

    def serialize(self):
        return {
            "user_id" : self.user_id,
            "stock_id" : self.stock_id
        }

class Portfolio(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )

    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="portfolio_user")

    stock_id = models.ForeignKey(
        Stock,
        on_delete=models.CASCADE,
        related_name="portfolio_stock")

    quantity = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    date = models.DateTimeField()

    def serialize(self):
        return {
            "user" : self.user_id,
            "stock_id" : self.stock_id,
            "quantity" : self.quantity,
            "price" : self.price,
            "date" : self.date,
        }

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

    def serialize(self):
        return {
            "date" : self.date_recorded.date(),
            "price" : self.price_close,
        }

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
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)

    def serialize(self):
        return {
        "date" : self.date.date(),
        "yhat" : self.yhat,
        "yhat_upper" : self.yhat_upper,
        "yhat_lower" : self.yhat_lower,
        "price" : self.price,
        }
