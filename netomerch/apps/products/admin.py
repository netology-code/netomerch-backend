from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from apps.products.models import Category, Item, ItemProperty, Review


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
    model = Item
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }


admin.site.register(Item, ItemAdmin)


class ReviewAdmin(admin.ModelAdmin):
    model = Review


admin.site.register(Review, ReviewAdmin)
