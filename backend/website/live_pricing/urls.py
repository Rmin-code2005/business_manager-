from django.urls import path

from .views import (
    all_currency_prices,
    symbol_currency_price,
    all_gold_prices,
    symbol_gold_price,
    all_crypto_prices,
    symbol_crypto_price
)

urlpatterns = [
    path(
        "currency/prices/",
        all_currency_prices,
        name="currency-all-prices",
    ),
    path(
        "currency/prices/<str:symbol>/",
        symbol_currency_price,
        name="currency-symbol-price",
    ),
    path(
        "gold/prices/",
        all_gold_prices,
        name="gold-all-prices",
    ),
    path(
        'gold/prices/<str:symbol>/',
        symbol_gold_price,
        name = 'gold-symbol-price'
    ),
    path(
        "crypto/prices/",
        all_crypto_prices,
        name="crypto-all-prices",
    ),
    path(
        'crypto/prices/<str:symbol>/',
        symbol_crypto_price,
        name = 'crypto-symbol-price'
    )
]