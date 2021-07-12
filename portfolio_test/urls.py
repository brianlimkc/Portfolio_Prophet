from django.urls import path
from portfolio_test.views import *

urlpatterns = [
    path('show', show_stock, name="show_stock"),
    path('get_stocks', populate_stock_history, name='populate_stock_history')
]