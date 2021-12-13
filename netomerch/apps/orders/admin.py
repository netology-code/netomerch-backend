from django.conf import settings
from django.contrib import admin
from django.db.models.fields import NullBooleanField
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from apps.orders.models import ItemConnections, Order
from apps.products.models import ImageColorItem, Item


class ItemInline(admin.TabularInline):

    model = Item.orders.through
    can_delete = True
    verbose_name = _('Item info')
    verbose_name_plural = _('Item info')
    fields = ['name', 'description', 'price', 'count']
    readonly_fields = ('name', 'description', 'price',)
    extra = 0

    def name(self, obj):
        return obj.items.name

    def description(self, obj):
        return obj.items.short_description

    def price(self, obj):
        return obj.items.price

    def count(self, obj):
        return obj.items.id.count()


@admin.register(Order)
class OrdersAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ("order_number", "item_count", "total_sum", "final_sum",
                       "discount", "name", "email", "phone", "comment", "create_date",)
    exclude = ('items',)
    inlines = [ItemInline]
    save_on_top = True

    list_display = ("order_number", "create_date", "name", "email", "phone", "item_count", "final_sum")

    fieldsets = (
        (
            _("Order info"),
            {"fields": ("order_number", "create_date", "item_count", "total_sum", "final_sum", "discount", "status")},
        ),
        (
            _("Client info"),
            {"fields": ("name", "email", "phone", "address", "comment")},
        ),
    )

    @admin.display(description=_('Order number'))
    def order_number(self, obj):
        return f'Заказ № {obj.id}'

    @admin.display(description=_('Item count'))
    def item_count(self, obj):
        from django.db.models import Sum
        items_count = ItemConnections.objects.filter(orders__pk=obj.id).aggregate(Sum('count'))['count__sum']
        return items_count
