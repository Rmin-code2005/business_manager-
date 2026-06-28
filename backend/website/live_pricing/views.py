from asgiref.sync import async_to_sync

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView , RetrieveAPIView

from drf_spectacular.utils import extend_schema

from .models import (
    CashBasket,
    GoldBasket,
    CryptoBasket,
)

from .serializers import (
    CurrencyBasketSerializer,
    GoldBasketSerializer,
    CryptoBasketSerializer,
    GeneralCryptoBasketSerializer,
    GeneralCurrencyBasketSerializer,
    GeneralGoldBasketSerializer
)

from .services import (
    get_all_currency_prices,
    get_price_by_symbol,
    get_all_gold,
    get_gold_by_symbol,
    get_all_crypto,
    get_crypto_by_symbol,
)

from .validator import (
    CURRENCY_SYMBOLS,
    GOLD_SYMBOLS,
    CRYPTO_SYMBOLS,
)


# =========================
# Symbols
# =========================

class SymbolsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=dict)
    def get(self, request):
        return Response(
            {
                "currency": CURRENCY_SYMBOLS,
                "gold": GOLD_SYMBOLS,
                "crypto": CRYPTO_SYMBOLS,
            }
        )


# =========================
# Currency Prices
# =========================

class CurrencyPricesView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=dict)
    def get(self, request):
        return Response(
            async_to_sync(get_all_currency_prices)()
        )


class CurrencyPriceView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=dict)
    def get(self, request, symbol):
        return Response(
            async_to_sync(get_price_by_symbol)(symbol)
        )


# =========================
# Gold Prices
# =========================

class GoldPricesView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=dict)
    def get(self, request):
        return Response(
            async_to_sync(get_all_gold)()
        )


class GoldPriceView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=dict)
    def get(self, request, symbol):
        return Response(
            async_to_sync(get_gold_by_symbol)(symbol)
        )


# =========================
# Crypto Prices
# =========================

class CryptoPricesView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=dict)
    def get(self, request):
        return Response(
            async_to_sync(get_all_crypto)()
        )


class CryptoPriceView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=dict)
    def get(self, request, symbol):
        return Response(
            async_to_sync(get_crypto_by_symbol)(symbol)
        )


# =========================
# User Baskets
# =========================

class AllUserCurrencyBaskets(ListAPIView):
  
    serializer_class = GeneralCurrencyBasketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
       
        return (
            CashBasket.alive_objects
            .filter(user=self.request.user)
            .prefetch_related("prices")
        )


class AllUserGoldBaskets(ListAPIView):
    
    serializer_class = GeneralGoldBasketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        
        return (
            GoldBasket.alive_objects
            .filter(user=self.request.user)
            .prefetch_related("prices")
        )


class AllUserCryptoBaskets(ListAPIView):
   
    serializer_class = GeneralCryptoBasketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            CryptoBasket.alive_objects
            .filter(user=self.request.user)
            .prefetch_related("prices")
        )
class SpeceficCurrencyBasketView(RetrieveAPIView):
    serializer_class = CurrencyBasketSerializer
    def get_object(self ):
        return CashBasket.alive_objects.get(name = self.kwargs['symbol'])

class SpeceficGoldBasketView(RetrieveAPIView):
    serializer_class = GoldBasketSerializer
    def get_object(self ):
        return GoldBasket.alive_objects.get(name = self.kwargs['symbol'])
    
class SpeceficCryptoBasketView(RetrieveAPIView):
    serializer_class = CryptoBasketSerializer
    def get_object(self ):
        return CryptoBasket.alive_objects.get(name = self.kwargs['symbol'])