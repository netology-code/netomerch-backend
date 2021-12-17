from django.db import models
from django.db.models import constraints
from django.utils.translation import gettext_lazy as _


class XlsxUpload(models.Model):
    class Meta:
        verbose_name = "Импорт из xlsx"

    file = models.FileField(upload_to='imports')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    result = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.id}: {self.uploaded_at}"


class Size(models.Model):
    class Meta:
        verbose_name = "Классификатор размера"
        verbose_name_plural = "Классификатор размеров"
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.id}: {self.name}"


class Specialization(models.Model):
    class Meta:
        verbose_name = "Классификатор специализации"
        verbose_name_plural = "Классификатор специализаций"
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.id}: {self.name}"


class Category(models.Model):
    class Meta:
        verbose_name = "Классификатор категории"
        verbose_name_plural = "Классификатор категорий"

    name = models.CharField(max_length=50, null=False, default='')

    def __str__(self):
        return f"{self.id}: {self.name}"


class DictImageColor(models.Model):
    class Meta:
        verbose_name = _("Классификатор цвета")
        verbose_name_plural = _("Классификатор цветов")
    name = models.CharField(null=False, blank=False, max_length=20, verbose_name=_("цвет"))
    name_eng = models.CharField(null=True, max_length=20, verbose_name=_("цвет по-английски"))
    color_code = models.CharField(null=False, max_length=7, default='#000000', verbose_name="код цвета")

    def __str__(self):
        result = f"{self.id}:{self.name}"
        if self.name_eng:
            result += f"({self.name_eng})"
        result += f" - {self.color_code}"
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
    specialization = models.ForeignKey(Specialization, null=True, related_name="item", on_delete=models.PROTECT)
    size = models.ManyToManyField(Size, related_name="item")
    imagecolor = models.ManyToManyField(DictImageColor, through="ImageColorItem", related_name="itemimagecolor")
    is_published = models.BooleanField(default=True)
    is_hit = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id}: {self.name}"


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
