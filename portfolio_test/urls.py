from django.urls import path
from portfolio_test.views import *

urlpatterns = [
    path('show', show_stock, name="show_stock"),
]