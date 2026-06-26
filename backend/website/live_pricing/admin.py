from django.contrib import admin

from .models import (
    Price,
    CashBasket,
    GoldBasket,
    CryptoBasket,
)


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "start_price_T",
        "start_price_D",
    )

    ordering = ("-id",)

    search_fields = (
        "id",
    )

    readonly_fields = (
        "start_price_T",
        "start_price_D",
    )

    def has_add_permission(self, request):
        return False


class BaseBasketAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "name",
        "count",
        "start_price_t",
        "start_price_d",
    )

    search_fields = (
        "name",
        "user__email",
        "user__phone",
    )

    list_filter = (
        "name",
    )

    ordering = (
        "user",
        "name",
    )

    autocomplete_fields = (
        "user",
    )

    readonly_fields = (
        "price",
    )

    @admin.display(description="Start Price (T)")
    def start_price_t(self, obj):
        if obj.price:
            return obj.price.start_price_T
        return "-"

    @admin.display(description="Start Price ($)")
    def start_price_d(self, obj):
        if obj.price:
            return obj.price.start_price_D
        return "-"


@admin.register(CashBasket)
class CashBasketAdmin(BaseBasketAdmin):
    pass


@admin.register(GoldBasket)
class GoldBasketAdmin(BaseBasketAdmin):
    pass


@admin.register(CryptoBasket)
class CryptoBasketAdmin(BaseBasketAdmin):
    pass