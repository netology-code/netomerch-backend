from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from apps.products.models import Category, ItemJSON, ItemProperty


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }


admin.site.register(Category, CategoryAdmin)


class ItemPropertyAdmin(admin.ModelAdmin):
    model = ItemProperty


admin.site.register(ItemProperty, ItemPropertyAdmin)


class ItemJSONAdmin(admin.ModelAdmin):
    model = ItemJSON
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }


admin.site.register(ItemJSON, ItemJSONAdmin)
