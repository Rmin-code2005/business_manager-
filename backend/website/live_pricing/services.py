from .clients import NerkhClient
from rest_framework.exceptions import NotFound
async def get_all_currency_prices():
    client = NerkhClient()
    
    return await client.get("/v1/prices/json/currency") 

async def get_price_by_symbol(symbol: str):
    data = await get_all_currency_prices()

    prices = data["data"]["prices"]

    symbol = symbol.upper()

    if symbol not in prices:
        raise NotFound(
            detail=f"Currency '{symbol}' not found."
        )

    return {
        "symbol": symbol,
        "price": prices[symbol]
    }

async def get_all_gold():
    client = NerkhClient()
    return await client.get("/v1/prices/json/gold")

async def get_gold_by_symbol(symbol:str):
    data = await get_all_gold()
    prices = data["data"]["prices"]

    symbol = symbol.upper()

    if symbol not in prices:
        raise NotFound(
            detail=f"Currency '{symbol}' not found."
        )

    return {
        "symbol": symbol,
        "price": prices[symbol]
    }
