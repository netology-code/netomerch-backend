from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from apps.products.models import Category, Image, Item, ItemProperty


class ImageAdmin(admin.StackedInline):
    model = Image.items.through
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }


admin.site.register(Category, CategoryAdmin)


class ItemPropertyAdmin(admin.ModelAdmin):
    model = ItemProperty


admin.site.register(ItemProperty, ItemPropertyAdmin)


class ItemAdmin(admin.ModelAdmin):
    inlines = [ImageAdmin]

    exclude = ['image']

    model = Item
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }


admin.site.register(Item, ItemAdmin)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass
