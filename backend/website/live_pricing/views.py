from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes
from .services import get_all_currency_prices , get_price_by_symbol
from rest_framework.permissions import IsAuthenticated
from asgiref.sync import async_to_sync
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def all_prices(request):
    data = async_to_sync(get_all_currency_prices)()
    return Response(data)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def symbol_price(request , symbol):
    data = async_to_sync( get_price_by_symbol)(symbol)
    return Response(data)