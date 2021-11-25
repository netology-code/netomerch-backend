from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from apps.orders.models import Order
from apps.products.models import Item
from apps.orders.models import ItemConnections


class ItemInline(admin.TabularInline):
    model = Item.orders.through
    fields = ['name', 'description', 'price', 'count', 'image']
    readonly_fields = ('name', 'description', 'price', 'count', 'image',)
    extra = 0

    def name(self, obj):
        return obj.items.name

    def description(self, obj):
        return obj.items.short_description

    def price(self, obj):
        return obj.items.price

    def count(self, obj):
        return obj.items.id.count()

    def image(self, obj):
        if obj.items.image:
            return mark_safe(f"<img src='{obj.items.image.url}' width=50>")

    image.short_description = 'Миниатюра'

    can_delete = False
    verbose_name = _('Item info')
    verbose_name_plural = _('Item info')


@admin.register(Order)
class OrdersAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ("order_number", "item_count", "order_sum", "name", "email", "phone")
    exclude = ('items',)
    inlines = [ItemInline]
    save_on_top = True

    list_display = ("order_number", "name", "email", "phone", "item_count", "order_sum")

    fieldsets = (
        (
            _("Order info"),
            {"fields": ("order_number", "item_count", "order_sum", "status")},
        ),
        (
            _("Client info"),
            {"fields": ("name", "email", "phone")},
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

    @admin.display(description=_('Order sum'))
    def order_sum(self, obj):
        items = Item.objects.filter(orders__pk=obj.id).values_list('id', 'price')

        main_sum = 0
        for item in items:
            cnt = ItemConnections.objects.filter(orders=obj.id).filter(items=item[0]).values_list('count', flat=True)[0]
            main_sum += item[1] * cnt

        return main_sum
