from rest_framework import serializers
from .models import CashBasket , GoldBasket , CryptoBasket


from rest_framework import serializers


class BaseBasketSerializer(serializers.ModelSerializer):
    start_price_t = serializers.ReadOnlyField(source="price.start_price_T")
    start_price_d = serializers.ReadOnlyField(source="price.start_price_D")

    class Meta:
        fields = (
            "name",
            "count",
            "start_price_t",
            "start_price_d",
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