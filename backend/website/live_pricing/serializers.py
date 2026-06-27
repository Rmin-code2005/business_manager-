from rest_framework import serializers
from .models import CashBasket , GoldBasket , CryptoBasket


from rest_framework import serializers


class BaseBasketSerializer(serializers.ModelSerializer):
    start_price_T = serializers.ReadOnlyField(source="price.start_price_T")
    start_price_D = serializers.ReadOnlyField(source="price.start_price_D")

    class Meta:
        fields = (
            "name",
            "count",
            "start_price_T",
            "start_price_D",
        )
class BaseGeneralBasketSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "name",
        )
        
class CurrencyBasketSerializer(BaseBasketSerializer):
    class Meta(BaseBasketSerializer.Meta):
        model = CashBasket 
        
        
class CryptoBasketSerializer(BaseBasketSerializer):
    class Meta(BaseBasketSerializer.Meta):
        model = CryptoBasket
        
class GoldBasketSerializer(BaseBasketSerializer):
    class Meta(BaseBasketSerializer.Meta):
        model = GoldBasket
        
        
class GeneralCurrencyBasketSerializer(BaseGeneralBasketSerializer):
    class Meta(BaseGeneralBasketSerializer.Meta):
        model = CashBasket 
        
        
class GeneralCryptoBasketSerializer(BaseGeneralBasketSerializer):
    class Meta(BaseGeneralBasketSerializer.Meta):
        model = CryptoBasket
        
class GeneralGoldBasketSerializer(BaseGeneralBasketSerializer):
    class Meta(BaseGeneralBasketSerializer.Meta):
        model = GoldBasket