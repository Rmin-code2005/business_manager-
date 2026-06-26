from django.db import models
from accounts.models import CustomUser
from .validator import (
    validate_gold_symbol,
    validate_crypto_symbol,
    validate_currency_symbol,
)

        
        
class Price(models.Model):
    start_price_T = models.DecimalField(
        max_digits=20,
        decimal_places=8
    )
    start_price_D = models.DecimalField(
        max_digits=20,
        decimal_places=8
    )

class BaseBasket(models.Model):
    count = models.FloatField()
    
    price = models.OneToOneField(
        Price ,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,)
    class Meta:
        abstract = True
    def __str__(self):
        return f"{self.name}"
    
class CashBasket(BaseBasket):
    user = models.ForeignKey(CustomUser , on_delete=models.CASCADE , related_name="cash_baskets")
    name = models.CharField(
        max_length=10,
        validators=[validate_currency_symbol],
    )
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name"],
                name="cashbasket_unique_symbol_per_user",
            )
        ]

class GoldBasket(BaseBasket):
    user = models.ForeignKey(CustomUser , on_delete=models.CASCADE , related_name="gold_baskets")
    name = models.CharField(
        max_length=10,
        validators=[validate_gold_symbol],
    )
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name"],
                name="goldbasket_unique_symbol_per_user",
            )
        ]
    
class CryptoBasket(BaseBasket):
    user = models.ForeignKey(CustomUser , on_delete=models.CASCADE , related_name="crypto_baskets")
    name = models.CharField(
        max_length=10,
        validators=[validate_crypto_symbol],
    )
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name"],
                name="cryptobasket_unique_symbol_per_user",
            )
        ]