from decimal import Decimal

from asgiref.sync import async_to_sync
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from live_pricing.services import get_price_by_symbol

from .models import (
    CashBasket,
    GoldBasket,
    CryptoBasket,
    Price,
)


def create_price(instance):
    asset_price = async_to_sync(get_price_by_symbol)(instance.name)
    usd_price = async_to_sync(get_price_by_symbol)("USD")

    price = Price.objects.create(
        start_price_T=Decimal(asset_price["price"]) * Decimal(instance.count),
        start_price_D=(
            Decimal(asset_price["price"]) * Decimal(instance.count)
            / Decimal(usd_price["price"])
        ),
    )

    instance.price = price
    instance.save(update_fields=["price"])


@receiver(post_save, sender=CashBasket)
@receiver(post_save, sender=GoldBasket)
@receiver(post_save, sender=CryptoBasket)
def create_price_signal(sender, instance, created, **kwargs):
    if created and instance.price_id is None:
        create_price(instance)


@receiver(post_delete, sender=CashBasket)
@receiver(post_delete, sender=GoldBasket)
@receiver(post_delete, sender=CryptoBasket)
def delete_price_signal(sender, instance, **kwargs):
    if instance.price_id:
        instance.price.delete()