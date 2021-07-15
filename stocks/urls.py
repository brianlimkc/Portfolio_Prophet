from django.urls import path
from stocks.views import *

urlpatterns = [
    path('show/', show_stock, name="show_stock"),
    path('show_all/', show_all, name="show_all"),
    path('get_stocks/', populate_stock_history, name='populate_stock_history'),
    path('populate/', populate_stocksdb, name="populate_stocksdb"),
    path('portfolio/', portfolio, name="portfolio"),
    path('watchlist/', watchlist, name="watchlist"),
    path('portfolio_delete/', portfolio_delete, name="portfolio_delete"),
    path('watchlist_delete/', watchlist_delete, name="watchlist_delete"),
]