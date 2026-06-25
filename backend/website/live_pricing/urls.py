from django.urls import path

from .views import (
    all_prices,
    symbol_price,
)

urlpatterns = [
    path(
        "prices/",
        all_prices,
        name="all-prices",
    ),
    path(
        "prices/<str:symbol>/",
        symbol_price,
        name="symbol-price",
    ),
]