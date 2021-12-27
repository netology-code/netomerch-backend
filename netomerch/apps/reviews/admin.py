from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.reviews.models import Review

# Register your models here.


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    model = Review

    save_on_top = True
    readonly_fields = ('dt_created',)

    list_display = ("order_number", "item", "dt_created", "is_published")
    list_filter = ('is_published',)

    fieldsets = (
        (
            _("Информация по товару"),
            {"fields": ("order", "item")},
        ),
        (
            _("Информация об авторе"),
            {"fields": ("author", "email")},
        ),
        (
            _("Информация об отзыве"),
            {"fields": ("text", "dt_created", "image")},
        ),
    )

    @admin.display(description=_('Номер заказа'))
    def order_number(self, obj):
        return f'Заказ №{obj.order.id}'
