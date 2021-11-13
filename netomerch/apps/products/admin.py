from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.products.models import Category, Item, ItemSpecProperty, SpecProperty


class CategoryAdmin(admin.ModelAdmin):
    model = Category

    list_display = (
        "category_name",
        "tag_list",
        "short_description",
        "description",
        "image",
    )
    fieldsets = (
        (
            _("Category info:"),
            {"fields": ("category_name", "tags", ("short_description", "description"), "image", )},
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return ", ".join(o.name for o in obj.tags.all())


class ItemAdmin(admin.ModelAdmin):
    model = Item

    list_display = (
        "category_id",
        "default_price",
        "item_name",
        "short_description",
        "description",
        "image",
        "is_published"
    )
    fieldsets = (
        (
            _("Item info:"),
            {"fields": (
                ("category_id", "item_name", "default_price", "image"),
                ("short_description", "description"), "is_published")},
        ),
    )


class SpecPropertyAdmin(admin.ModelAdmin):
    model = SpecProperty


class ItemSpecPropertyAdmin(admin.ModelAdmin):
    model = ItemSpecProperty

    list_display = (
        "item_id",
        "spec_property_id",
        "d_value",
        "s_value",
        "n_value",
        "text_value",
    )
    fieldsets = (
        (
            _("Special property info:"),
            {"fields": (
                ("item_id", "spec_property_id"),
                ("n_value", "s_value", "d_value"),
                "text_value")
             },
        ),
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(SpecProperty, SpecPropertyAdmin)
admin.site.register(ItemSpecProperty, ItemSpecPropertyAdmin)
