from django.contrib import admin

from .models import Bill, BillItem, Denomination, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("product_id", "name", "stock", "unit_price", "tax_percent")
    search_fields = ("product_id", "name")


@admin.register(Denomination)
class DenominationAdmin(admin.ModelAdmin):
    list_display = ("value", "count")


class BillItemInline(admin.TabularInline):
    model = BillItem
    readonly_fields = ("unit_price", "tax_percent", "line_total")
    extra = 0


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer_email",
        "created_at",
        "total_amount",
        "paid_amount",
        "change_amount",
    )
    inlines = [BillItemInline]
    readonly_fields = ("created_at",)
