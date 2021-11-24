from django.contrib import admin

from apps.orders.models import Order
from apps.products.models import Item


class ItemInLine(admin.TabularInline):
    model = Order.items.through


@admin.register(Order)
class OrdersAdmin(admin.ModelAdmin):
    model = Order
    inlines = [
        ItemInLine,
    ]
    exclude = ('items',)
    list_display = ("order_number", "name", "email", "phone", "item_count")

    def order_number(self, obj):
        return f'Заказ № {obj.id}'

    def item_count(self, obj):
        items_count = Item.objects.filter(orders__pk=obj.id).count()
        return items_count




