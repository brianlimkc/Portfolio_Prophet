from django.urls import path
from portfolio_test.views import *

urlpatterns = [
    path('show/<str:stock>', show_stock, name="show_stock"),
]