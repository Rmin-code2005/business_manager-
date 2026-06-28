from rest_framework import serializers
from django.db.models import Sum
from .models import CashBasket, GoldBasket, CryptoBasket, Price


class PriceLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = (
            "id",
            "count",
            "start_price_T",
            "start_price_D",
            "created_at",
        )


class BaseBasketSerializer(serializers.ModelSerializer):
    start_price_T = serializers.SerializerMethodField()
    start_price_D = serializers.SerializerMethodField()
    # در صورت نیاز می‌توانید تاریخچه تغییرات قیمت این بسکت را هم در خروجی ببینید:
    price_logs = PriceLogSerializer(source="prices", many=True, read_only=True)

    class Meta:
        fields = (
            "id",
            "name",
            "count",
            "start_price_T",
            "start_price_D",
            "price_logs",
        )

    def get_start_price_T(self, obj):
        # جمع مبالغ تومانی تمام تراکنش‌های فعال این بسکت
        result = obj.prices.filter(is_deleted=False).aggregate(total=Sum('start_price_T'))
        return result['total'] or 0.0

    def get_start_price_D(self, obj):
        # جمع مبالغ دلاری تمام تراکنش‌های فعال این بسکت
        result = obj.prices.filter(is_deleted=False).aggregate(total=Sum('start_price_D'))
        return result['total'] or 0.0


class BaseGeneralBasketSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name",)


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