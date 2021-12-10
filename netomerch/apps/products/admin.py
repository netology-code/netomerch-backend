from django.contrib import admin
from django.utils.safestring import mark_safe

from apps.products.models import Category, Color, Image, Item, ItemColor, ItemColorImage, Size, Specialization


class ItemSizeAdmin(admin.TabularInline):
    model = Color.item.through
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category

    list_display = ("name", "cat_photo")

    def cat_photo(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width=50>")


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = [ItemSizeAdmin]

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
    ordering = ['item']
    inlines = [ItemColorImageAdmin]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass
