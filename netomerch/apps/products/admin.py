from django.conf import settings
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
    fieldsets = (
        (None,                          {'fields': ('name', 'price')}),
        ('Category, Specializations:',  {'fields': ('category', 'specialization')}),
        ('Desscription:',               {'fields': ('description', 'short_description')}),
        ('Flags:',                      {'fields': ('is_published', 'is_hit'), 'classes': ('collapse',)}),
        # ('Sizes:',                      {'fields': ('size',)}),
        # ('Colors and images:',          {'fields': ('color',)})
    )

    model = Item


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    model = Specialization

    list_display = ("name", "spec_image")
    readonly_fields = ('name', 'spec_image',)

    def spec_image(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width=50>")


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
