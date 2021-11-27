from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from apps.orders.models import ItemConnections, Order
from apps.products.models import Image, Item


class ItemInline(admin.TabularInline):

    model = Item.orders.through
    fields = ['name', 'description', 'price', 'count', 'image']
    readonly_fields = ('name', 'description', 'price', 'image',)
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
        item_id = obj.items.id
        image = Image.objects.filter(items=item_id).values_list('image', flat=True)[0]
        url = settings.MEDIA_URL + image
        if image:
            return mark_safe(f"<img src='{url}' width=50>")

    image.short_description = _('Miniature')

    can_delete = True
    verbose_name = _('Item info')
    verbose_name_plural = _('Item info')


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
