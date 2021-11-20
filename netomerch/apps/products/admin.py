from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from apps.products.models import CategoryJSON, ItemJSON, SpecProperty


class SpecPropertyAdmin(admin.ModelAdmin):
    model = SpecProperty


admin.site.register(SpecProperty, SpecPropertyAdmin)


class ItemJSONAdmin(admin.ModelAdmin):
    model = ItemJSON
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }


class CategoryJSONAdmin(admin.ModelAdmin):
    model = CategoryJSON
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }


admin.site.register(ItemJSON, ItemJSONAdmin)
admin.site.register(CategoryJSON, CategoryJSONAdmin)
