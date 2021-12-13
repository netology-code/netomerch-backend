from django.db import models
from django.db.models import constraints
from django.utils.translation import gettext_lazy as _


class Size(models.Model):
    class Meta:
        verbose_name = "Размер"
        verbose_name_plural = "Размеры"
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.id}: name {self.name}"


# class Color(models.Model):
#     class Meta:
#         verbose_name = "Цвет"
#         verbose_name_plural = "Цвета"
#     name = models.CharField(max_length=20)

#     def __str__(self):
#         return f"{self.id}: name {self.name}"


class Specialization(models.Model):
    class Meta:
        verbose_name = "Направление"
        verbose_name_plural = "Направления"
    name = models.CharField(max_length=50)
    image = models.ImageField(blank=True, null=True, upload_to='categories')

    def __str__(self):
        return f"{self.id}: name {self.name}"


class Category(models.Model):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    name = models.CharField(max_length=50, null=False, default='')
    image = models.ImageField(blank=True, null=True, upload_to='categories')

    def __str__(self):
        return f"{self.id}: name {self.name}"


class DictImageColor(models.Model):
    class Meta:
        verbose_name = _("Классификатор цвета")
        verbose_name_plural = _("Классификатор цветов")
    name = models.CharField(null=False, blank=False, max_length=20, verbose_name=_("цвет"))
    name_eng = models.CharField(null=True, max_length=20, verbose_name=_("цвет по-английски"))
    image = models.ImageField(upload_to='colors', verbose_name=_("изображение цвета"))

    def __str__(self):
        result = f"{self.id}:{self.name}"
        if self.name_eng:
            result += f"({self.name_eng})"
        return result


class Item(models.Model):
    class Meta:
        verbose_name = _("Товар")
        verbose_name_plural = _("Товары")

    name = models.CharField(max_length=50, default='')
    short_description = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=13, decimal_places=2, default=0.00)
    category = models.ForeignKey(Category, null=True, related_name="item", on_delete=models.PROTECT)
    specialization = models.ManyToManyField(Specialization, related_name="item")
    # color = models.ManyToManyField(Color, through='ItemColor', related_name="itemcolor")
    size = models.ManyToManyField(Size, related_name="item")
    # imagecolor = models.ManyToManyField()
    imagecolor = models.ManyToManyField("ImageColorItem", related_name="itemimagecolor")
    is_published = models.BooleanField(default=True)
    is_hit = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id}: name {self.name}"


class ImageColorItem(models.Model):
    class Meta:
        verbose_name = _("Изображение цвета товара")
        verbose_name_plural = _("Изображения цвета товара")
        constraints.CheckConstraint(
            name="%(app_label)s_%(class)s_is_main_color_present",
            check=models.Q(is_main_color__eq=True)
        )

    item = models.ForeignKey(Item, related_name="onitem", on_delete=models.PROTECT)
    color = models.ForeignKey(DictImageColor, related_name="oncolor", on_delete=models.PROTECT)
    image = models.ImageField(upload_to='item', blank=True, null=True)
    is_main_color = models.BooleanField(default=False, verbose_name=_("основной цвет"))
    is_main_image = models.BooleanField(default=False, verbose_name=_("основная картинка"))

    def __str__(self) -> str:
        return f"{self.id}: {self.item}"


class Image(models.Model):
    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"

    image = models.ImageField(upload_to='item', blank=True, null=True)
    is_main = models.BooleanField(default=False)


# class ItemColor(models.Model):
#     class Meta:
#         verbose_name = "Цвет товара"
#         verbose_name_plural = "Цвета товара"

#     item = models.ForeignKey(Item, on_delete=models.PROTECT)
#     color = models.ForeignKey(Color, on_delete=models.PROTECT, related_name='itemcolorcolor')
#     images = models.ManyToManyField(Image)
#     is_main = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.item.name} - {self.color.name}"


# class ItemColorImage(models.Model):
#     itemcolor = models.ForeignKey(ItemColor, related_name="image", on_delete=models.PROTECT)
#     item = models.ForeignKey(Item, default=None, on_delete=models.PROTECT)
#     image = models.ForeignKey(Image, on_delete=models.PROTECT)
