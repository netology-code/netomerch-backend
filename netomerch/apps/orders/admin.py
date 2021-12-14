from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.orders.models import ItemConnections, Order, Promocode
from apps.products.models import Item


@admin.register(Promocode)
class Promocode(admin.ModelAdmin):
    model = Promocode


class ItemInline(admin.TabularInline):

    model = Item.orders.through
    fields = ['name', 'item_color', 'item_size', 'item_price', 'count']
    readonly_fields = ('name', 'item_color', 'item_size', 'item_price',)

    extra = 0

    def name(self, obj):
        return obj.item.name

    def item_color(self, obj):
        return obj.color

    def item_price(self, obj):
        return obj.price

    def item_size(self, obj):
        return obj.size

    def count(self, obj):
        return obj.item.id.count()


    can_delete = True
    verbose_name = _('Инфорация о товарах')
    verbose_name_plural = _('Информация о товарах')


@admin.register(Order)
class OrdersAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ("order_number", "item_count", "total_sum", "final_sum",
                       "name", "email", "phone", "comment", "create_date", "promo_status",)
    exclude = ('items',)
    inlines = [ItemInline]
    save_on_top = True

    list_display = ("order_number", "create_date", "name", "email", "phone", "item_count", "final_sum")

    fieldsets = (
        (
            _("Информация по заказу"),
            {"fields": ("order_number", "create_date", "item_count", "total_sum", "final_sum", "status", "promo_status")},
        ),
        (
            _("Информация о клиенте"),
            {"fields": ("name", "email", "phone", "address", "comment")},
        ),
    )

    @admin.display(description=_('Номер заказа'))
    def order_number(self, obj):
        return f'Заказ № {obj.id}'

    @admin.display(description=_('Кол-во товаров'))
    def item_count(self, obj):
        from django.db.models import Sum
        items_count = ItemConnections.objects.filter(order__pk=obj.id).aggregate(Sum('count'))['count__sum']
        return items_count

    @admin.display(description=_('Промокод'))
    def promo_status(self, obj):
        if obj.promocode:
            return f'Да'
        else:
            return f'Нет'
