from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from apps.products.models import Category, ItemJSON, SpecProperty


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }


admin.site.register(Category, CategoryAdmin)


class SpecPropertyAdmin(admin.ModelAdmin):
    model = SpecProperty


admin.site.register(SpecProperty, SpecPropertyAdmin)


class ItemJSONAdmin(admin.ModelAdmin):
    model = ItemJSON
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }


admin.site.register(ItemJSON, ItemJSONAdmin)
