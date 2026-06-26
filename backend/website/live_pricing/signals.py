from decimal import Decimal

from asgiref.sync import async_to_sync
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from live_pricing.services import get_price_by_symbol

from .models import CashBasket, GoldBasket, CryptoBasket, Price


# -----------------------------
# Price Helpers
# -----------------------------

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

    type(instance).objects.filter(pk=instance.pk).update(price=price)
    instance.price = price


def update_price(instance):
    delta = Decimal(instance.count) - instance._old_count

    if delta == 0:
        return

    asset_price = async_to_sync(get_price_by_symbol)(instance.name)
    usd_price = async_to_sync(get_price_by_symbol)("USD")

    instance.price.start_price_T += Decimal(asset_price["price"]) * delta
    instance.price.start_price_D += (
        Decimal(asset_price["price"]) * delta
        / Decimal(usd_price["price"])
    )

    instance.price.save(
        update_fields=["start_price_T", "start_price_D"]
    )


# -----------------------------
# Pre Save (track old state)
# -----------------------------

@receiver(pre_save, sender=CashBasket)
@receiver(pre_save, sender=GoldBasket)
@receiver(pre_save, sender=CryptoBasket)
def remember_old_state(sender, instance, **kwargs):

    if not instance.pk:
        instance._old_count = Decimal("0")
        instance._old_is_deleted = False
        return

    old = sender.objects.filter(pk=instance.pk).first()

    if old is None:
        instance._old_count = Decimal("0")
        instance._old_is_deleted = False
        return

    instance._old_count = Decimal(old.count)
    instance._old_is_deleted = old.is_deleted


# -----------------------------
# Post Save (main logic)
# -----------------------------

@receiver(post_save, sender=CashBasket)
@receiver(post_save, sender=GoldBasket)
@receiver(post_save, sender=CryptoBasket)
def price_signal(sender, instance, created, **kwargs):

    # 1. CREATE
    if created:
        create_price(instance)
        return

    # 2. SOFT DELETE
    if instance.is_deleted and not instance._old_is_deleted:
        if instance.price:
            instance.price.delete()
        return

    # 3. RESTORE
    if not instance.is_deleted and instance._old_is_deleted:
        if instance.price and instance.price.is_deleted:
            instance.price.restore()
        return

    # 4. ignore deleted objects
    if instance.is_deleted:
        return

    # 5. price missing safety
    if instance.price_id is None:
        return

    # 6. COUNT UPDATE
    if Decimal(instance.count) != instance._old_count:
        update_price(instance)