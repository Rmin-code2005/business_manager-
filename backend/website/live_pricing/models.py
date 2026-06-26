from django.db import models
from django.utils import timezone

from accounts.models import CustomUser

from .managers import AliveObjects
from .validator import (
    validate_currency_symbol,
    validate_gold_symbol,
    validate_crypto_symbol,
)


# -----------------------------
# Abstract Models
# -----------------------------


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    objects = models.Manager()
    alive_objects = AliveObjects()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """
        Soft Delete
        """
        if self.is_deleted:
            return

        self.is_deleted = True
        self.deleted_at = timezone.now()

        self.save(update_fields=[
            "is_deleted",
            "deleted_at",
        ])

    def restore(self):
        """
        Restore Soft Deleted Object
        """
        if not self.is_deleted:
            return

        self.is_deleted = False
        self.deleted_at = None

        self.save(update_fields=[
            "is_deleted",
            "deleted_at",
        ])

    def hard_delete(self, using=None, keep_parents=False):
        """
        Physical Delete
        """
        super().delete(using=using, keep_parents=keep_parents)


# -----------------------------
# Price
# -----------------------------


class Price(TimeStampedModel, SoftDeleteModel):
    start_price_T = models.DecimalField(
        max_digits=20,
        decimal_places=8,
    )

    start_price_D = models.DecimalField(
        max_digits=20,
        decimal_places=8,
    )

    def __str__(self):
        return f"{self.start_price_T}"
    


# -----------------------------
# Base Basket
# -----------------------------


class BaseBasket(TimeStampedModel, SoftDeleteModel):
    count = models.DecimalField(
        max_digits=20,
        decimal_places=8,
    )

    price = models.OneToOneField(
        Price,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        if self.price:
            self.price.delete()

        super().delete(using=using, keep_parents=keep_parents)

    def restore(self):
        if self.price:
            self.price.restore()

        super().restore()

    def hard_delete(self, using=None, keep_parents=False):
        """
        Hard delete basket + related price
        """
        if self.price:
            self.price.hard_delete()

        super().hard_delete(using=using, keep_parents=keep_parents)
    @property
    def total_price_t(self):
        return self.price.start_price_T if self.price else None
    @property
    def total_price_d(self):
        return self.price.start_price_D if self.price else None


# -----------------------------
# Cash Basket
# -----------------------------


class CashBasket(BaseBasket):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="cash_baskets",
    )

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


# -----------------------------
# Gold Basket
# -----------------------------


class GoldBasket(BaseBasket):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="gold_baskets",
    )

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


# -----------------------------
# Crypto Basket
# -----------------------------


class CryptoBasket(BaseBasket):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="crypto_baskets",
    )

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