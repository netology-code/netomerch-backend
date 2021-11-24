from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from apps.orders.models import Order
from apps.products.models import Item


class ItemInline(admin.TabularInline):
    model = Item.orders.through
    fields = ['name', 'description', 'price', 'image']
    readonly_fields = ('name', 'description', 'price', 'image',)
    extra = 0

    def name(self, obj):
        return obj.item.name

    def description(self, obj):
        return obj.item.short_description

    def price(self, obj):
        return obj.item.price

    def image(self, obj):
        if obj.item.image:
            return mark_safe(f"<img src='{obj.item.image.url}' width=50>")

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
        items_count = Item.objects.filter(orders__pk=obj.id).count()
        return items_count

    @admin.display(description=_('Order sum'))
    def order_sum(self, obj):
        from django.db.models import Sum
        main_sum = Item.objects.filter(orders__pk=obj.id).aggregate(Sum('price'))['price__sum']
        return main_sum
