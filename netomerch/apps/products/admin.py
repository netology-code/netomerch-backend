from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from apps.products.models import Category, Color, Image, Item, ItemColor, ItemColorImage, Size, Specialization


class ItemColorInlineAdmin(admin.TabularInline):
    def edit_photos(self, instance):
        url = reverse(f'admin:{instance._meta.app_label}_{instance._meta.model_name}_change',
                      args=[instance.pk])
        if instance.pk:
            return mark_safe(u'<a href="{u}">Изменить фото</a>'.format(u=url))
        else:
            return ''

    model = Color.item.through
    extra = 1
    readonly_fields = ('edit_photos',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category

    list_display = ("name", "cat_photo")

    def cat_photo(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width=50>")


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = [ItemColorInlineAdmin]

    list_display = ("name", "category", "price", "short_description")

    model = Item


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    pass


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    pass


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    pass


class ItemColorImageAdmin(admin.TabularInline):
    model = ItemColorImage
    extra = 1


@admin.register(ItemColor)
class ItemColorAdmin(admin.ModelAdmin):
    ordering = ['item', 'color']
    inlines = [ItemColorImageAdmin]
    list_filter = ['item', 'color']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass
