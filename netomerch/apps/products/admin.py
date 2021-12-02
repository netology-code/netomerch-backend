from django.conf import settings
from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe
from django_json_widget.widgets import JSONEditorWidget

from apps.products.models import Category, Image, Item


class ItemImageAdmin(admin.StackedInline):
    model = Image.items.through
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category

    list_display = ("name", "short_description", "description", "cat_photo")

    def cat_photo(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width=50>")


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = [ItemImageAdmin]

    exclude = ['image']

    list_display = ("name", "categories", "price", "short_description", "first_image")

    model = Item
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},  # TODO: Как изменим модель не забыть удалить
    }

    def categories(self, obj):
        categories = Category.objects.filter(item__pk=obj.id).values_list('name', flat=True)
        return ', '.join(categories)

    def first_image(self, obj):
        image = Image.objects.filter(items=obj.id).values_list('image', flat=True)
        if image:
            url = settings.MEDIA_URL + image[0]
            return mark_safe(f"<img src='{url}' width=50>")


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass
