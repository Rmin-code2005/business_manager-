from decimal import Decimal

from asgiref.sync import async_to_sync
from django.db.models.signals import pre_save, post_save, post_delete
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

    # update() سیگنال اجرا نمی‌کند
    type(instance).objects.filter(pk=instance.pk).update(price=price)

    # فقط برای اینکه آبجکت داخل حافظه هم آپدیت شود
    instance.price = price


def update_price(instance):
    delta = Decimal(instance.count) - instance._old_count

    if delta == 0:
        return

    asset_price = async_to_sync(get_price_by_symbol)(instance.name)
    usd_price = async_to_sync(get_price_by_symbol)("USD")

    instance.price.start_price_T += (
        Decimal(asset_price["price"]) * delta
    )

    instance.price.start_price_D += (
        Decimal(asset_price["price"]) * delta
        / Decimal(usd_price["price"])
    )

    instance.price.save(
        update_fields=[
            "start_price_T",
            "start_price_D",
        ]
    )


@receiver(pre_save, sender=CashBasket)
@receiver(pre_save, sender=GoldBasket)
@receiver(pre_save, sender=CryptoBasket)
def remember_old_count(sender, instance, **kwargs):
    if instance.pk is None:
        instance._old_count = Decimal("0")
        return

    old = sender.objects.get(pk=instance.pk)
    instance._old_count = Decimal(old.count)


@receiver(post_save, sender=CashBasket)
@receiver(post_save, sender=GoldBasket)
@receiver(post_save, sender=CryptoBasket)
def price_signal(sender, instance, created, **kwargs):

    if created:
        create_price(instance)
        return

    if instance.price_id is None:
        return

    if Decimal(instance.count) != instance._old_count:
        update_price(instance)


@receiver(post_delete, sender=CashBasket)
@receiver(post_delete, sender=GoldBasket)
@receiver(post_delete, sender=CryptoBasket)
def delete_price_signal(sender, instance, **kwargs):
    if instance.price_id:
        instance.price.delete()