from django.contrib import admin

from .models import (
    Price,
    CashBasket,
    GoldBasket,
    CryptoBasket,
)
from .filters import SoftDeleteFilter
from .actions import (
    soft_delete_baskets,
    restore_baskets,
    hard_delete_baskets,
)

@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        # مهم‌ترین قسمت
        return self.model.alive_objects.all()
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
        "deleted",
        "start_price_t",
        "start_price_d",
    )

    search_fields = (
        "name",
        "user__email",
        "user__phone",
    )

    ordering = (
        "-id",
    )

    autocomplete_fields = (
        "user",
    )

    readonly_fields = (
        "price",
    )

    list_filter = (
        SoftDeleteFilter,
        "name",
    )

    actions = (
        soft_delete_baskets,
        restore_baskets,
        hard_delete_baskets,
    )

    def get_queryset(self, request):
        # مهم‌ترین قسمت
        return self.model.objects.select_related(
            "user",
            "price",
        )

    @admin.display(boolean=True, description="Deleted")
    def deleted(self, obj):
        return obj.is_deleted

    @admin.display(description="Start Price (T)")
    def start_price_t(self, obj):
        return obj.price.start_price_T if obj.price else "-"

    @admin.display(description="Start Price ($)")
    def start_price_d(self, obj):
        return obj.price.start_price_D if obj.price else "-"

@admin.register(CashBasket)
class CashBasketAdmin(BaseBasketAdmin):
    pass


@admin.register(GoldBasket)
class GoldBasketAdmin(BaseBasketAdmin):
    pass


@admin.register(CryptoBasket)
class CryptoBasketAdmin(BaseBasketAdmin):
    pass