from rest_framework import serializers
from stocks.models import *

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class RecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historical_Stock_Data
        fields = '__all__'


class ForecastsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forecast_Record
        fields = '__all__'