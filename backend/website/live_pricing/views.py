from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes
from .services import get_all_currency_prices , get_price_by_symbol , get_all_gold , get_gold_by_symbol , get_all_crypto , get_crypto_by_symbol
from rest_framework.permissions import IsAuthenticated
from asgiref.sync import async_to_sync
from rest_framework.views import APIView 
from rest_framework.generics import GenericAPIView
from .validator import GOLD_SYMBOLS , CRYPTO_SYMBOLS , CURRENCY_SYMBOLS



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_currency_prices(request):
    data = async_to_sync(get_all_currency_prices)()
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def symbol_currency_price(request , symbol):
    data = async_to_sync( get_price_by_symbol)(symbol)
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_gold_prices(request):
    data = async_to_sync(get_all_gold)()
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def symbol_gold_price(request , symbol):
    data = async_to_sync(get_gold_by_symbol)(symbol)
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_crypto_prices(request):
    data = async_to_sync(get_all_crypto)()
    return Response(data)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def symbol_crypto_price(request , symbol):
    data = async_to_sync(get_crypto_by_symbol)(symbol)
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def symbolsView(request):
    return Response(
        {
            "currency": CURRENCY_SYMBOLS,
            "gold": GOLD_SYMBOLS,
            "crypto": CRYPTO_SYMBOLS,
        }
    )
