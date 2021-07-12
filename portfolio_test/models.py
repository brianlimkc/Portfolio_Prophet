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
    market_cap = models.DecimalField(default=0.00, decimal_places=2, max_digits=11,null=True)
    current_price = models.DecimalField(default=0.00, decimal_places=2, max_digits=7,null=True)
    volume = models.DecimalField(default=0.00, decimal_places=2, max_digits=11,null=True)
    prev_high = models.DecimalField(default=0.00, decimal_places=2, max_digits=7,null=True)
    prev_low = models.DecimalField(default=0.00, decimal_places=2, max_digits=7,null=True)
    price_change = models.DecimalField(default=0.00, decimal_places=2, max_digits=7,null=True)
    percent_change = models.DecimalField(default=0.00, decimal_places=2, max_digits=7,null=True)
    date_added = models.DateTimeField(auto_now_add=True,null=True)
    date_updated = models.DateTimeField(null=True)

    def __str__(self):
        return self.name


# class Stocks_Tracked(models.Model):
#     id = models.UUIDField(
#         primary_key=True,
#         editable=False,
#         default=uuid.uuid4
#     )    

#     stock_id = models.ForeignKey(
#         Stock, 
#         on_delete=models.CASCADE, 
#         related_name="stock_track_id")

#     symbol = models.CharField(max_length=10)
#     date_added = models.DateTimeField(auto_now_add=True)
#     date_updated = models.DateTimeField()

#     def __str__(self):
#         return self.stock_id.name


class Historical_Stock_Data(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )

    stock_id = models.ForeignKey(
        Stock, 
        on_delete=models.CASCADE, 
        related_name="stock_data_id")

    date_recorded = models.DateTimeField()
    price_open = models.DecimalField(default=0.00, decimal_places=2, max_digits=7)
    price_close = models.DecimalField(default=0.00, decimal_places=2, max_digits=7)
    price_high = models.DecimalField(default=0.00, decimal_places=2, max_digits=7)
    price_low = models.DecimalField(default=0.00, decimal_places=2, max_digits=7)
    volume = models.DecimalField(default=0.00, decimal_places=2, max_digits=11)


