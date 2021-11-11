from django.contrib import admin
from django.contrib.admin.helpers import Fieldset
from apps.products.models import Category, Item, SpecProperty
from django.utils.translation import gettext_lazy as _


class CategoryAdmin(admin.ModelAdmin):
    model = Category

    list_display = (
        "parent_id",
        "category_name",
        "short_description",
        "description",
        "image",
    )
    fieldsets = (
        # (None, {"fields": ("parent_id", "category_name", "short_description", "description", "image")}),
        (
            _("Category info:"),
            {"fields": ("parent_id", "category_name", ("short_description", "description"), "image", )},
        ),
    )


admin.site.register(Category, CategoryAdmin)
