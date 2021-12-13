from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from apps.orders.models import ItemConnections, Order
from apps.products.models import Image, Item, ItemColor, ItemColorImage


class ItemInline(admin.TabularInline):

    model = Item.order.through
    fields = ['name', 'description', 'price', 'count', 'image']
    readonly_fields = ('name', 'description', 'price', 'image',)
    extra = 0

    def name(self, obj):
        return obj.item.name

    def description(self, obj):
        return obj.item.short_description

    def price(self, obj):
        return obj.item.price

    def count(self, obj):
        return obj.item.id.count()

    def image(self, obj):
        item_id = obj.item.id
        color_id = obj.item.color
        item_color = ItemColor.objects.filter(item=item_id).filter(color=color_id).first()
        image = ItemColorImage.objects.filter(itemcolor=item_color).filter(is_main=True).first()
        if image:
            url = settings.MEDIA_URL + image[0]
            return mark_safe(f"<img src='{url}' width=50>")

    image.short_description = _('Миниатюра')

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
