from django import forms
from django.contrib import admin
from django.core import management
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from apps.products.models import Category, DictImageColor, ImageColorItem, Item, Size, Specialization, XlsxUpload


@admin.register(XlsxUpload)
class XlsxUploadAdmin(admin.ModelAdmin):
    model = XlsxUpload

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        obj.save()
        print(obj.file)
        management.call_command('load_products', obj.file.path)
        print(obj)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category

    # list_display = ("name",)


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    model = Specialization


class ItemSizeAdmin(admin.TabularInline):
    model = Size.item.through
    extra = 1


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    pass


@admin.register(DictImageColor)
class DictImageColorAdmin(admin.ModelAdmin):
    model = DictImageColor
    list_display = ("color",)

    def color(self, obj):
        result = f"{obj.id}: {obj.name}"
        if obj.name_eng:
            result += f" ({obj.name_eng})"
        result += f" - {obj.color_code}"
        back_color = ('#000000' if obj.color_code != '#000000' else '#FFFFFF')
        print(obj.id, result, back_color)
        return mark_safe(f"<span style='color:{obj.color_code}; background-color:{back_color}'>{result}</span>")


class ImageColorItemAdmin(admin.TabularInline):
    model = ImageColorItem


class MyItemAdminForm(forms.ModelForm):
    def check_main_color_present(self, total_forms):
        main_color_count = 0
        for color_row in range(total_forms):
            if self.data.get(f"onitem-{color_row}-is_main_color") == "on":
                main_color_count += 1

        if main_color_count == 0:
            raise ValidationError(_("Обязательно должен быть установлен основной цвет!"))
        elif main_color_count > 1:
            raise ValidationError(_("Основной цвет должен быть только один!"))

    def check_main_image_present(self, total_forms):
        colors = set([self.data.get(f"onitem-{color_row}-color") for color_row in range(total_forms)
                      if self.data.get(f"onitem-{color_row}-color") != ""])
        for color in colors:
            main_image_count = 0
            for color_row in range(total_forms):
                if self.data.get(f"onitem-{color_row}-color") == color \
                        and self.data.get(f"onitem-{color_row}-is_main_image") == "on":
                    main_image_count += 1

            if main_image_count == 0:
                color_name = DictImageColor.objects.get(id=color).name
                raise ValidationError(
                    _(f"Для цвета {color_name} с id={color} обязательно должно быть установлено основное изображение!"))
            elif main_image_count > 1:
                color_name = DictImageColor.objects.get(id=color).name
                raise ValidationError(
                    _(f"Для цвета {color_name} с id={color} должно быть только одно основное изображение!"))

    def clean(self):
        super().clean()
        total_forms = int(self.data.get("onitem-TOTAL_FORMS"))

        self.check_main_color_present(total_forms)
        self.check_main_image_present(total_forms)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    model = Item
    form = MyItemAdminForm
    inlines = (ImageColorItemAdmin, )

    list_display = ("name", "main_image", "category", "price", "short_description")
    fieldsets = (
        (None, {'fields': ('name', 'price')}),
        ('Category, Specializations:', {'fields': ('category', 'specialization')}),
        ('Desscription:', {'fields': ('description', 'short_description')}),
        ('Flags:', {'fields': ('is_published', 'is_hit'), 'classes': ('collapse',)}),
        ('Sizes:', {'fields': ('size',)}),
    )

    def main_image(self, obj):
        main_image = ImageColorItem.objects.get(item_id=obj.id, is_main_color=True, is_main_image=True).image
        if len(main_image.url) > 0:
            return mark_safe(f"<img src='{main_image.url}' width=50>")
        else:
            return "Нет изображения"
