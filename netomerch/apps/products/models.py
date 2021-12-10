from django.db import models
from taggit.managers import TaggableManager


class Size(models.Model):
    class Meta:
        verbose_name = "Размер"
        verbose_name_plural = "Размеры"
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.id}: name {self.name}"


class Color(models.Model):
    class Meta:
        verbose_name = "Цвет"
        verbose_name_plural = "Цвета"
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.id}: name {self.name}"


class Specialization(models.Model):
    class Meta:
        verbose_name = "Направление"
        verbose_name_plural = "Направления"
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='categories')

    def __str__(self):
        return f"{self.id}: name {self.name}"


class Category(models.Model):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    name = models.CharField(max_length=50, null=False, default='')
    description = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='categories')

    def __str__(self):
        return f"{self.id}: name {self.name}"


class Item(models.Model):
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    name = models.CharField(max_length=50, default='')
    short_description = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=13, decimal_places=2, default=0.00)
    category = models.ForeignKey(Category, null=True, related_name="item", on_delete=models.PROTECT)
    specialization = models.ManyToManyField(Specialization, related_name="item")
    color = models.ManyToManyField(Color, through='ItemColor', related_name="item")
    size = models.ManyToManyField(Size, related_name="item")
    is_published = models.BooleanField(default=False)
    tags = TaggableManager(blank=True)
    is_hit = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id}: name {self.name}"


class ItemColor(models.Model):
    class Meta:
        verbose_name = "Цвет товара"
        verbose_name_plural = "Цвета товара"

    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    color = models.ForeignKey(Color, on_delete=models.PROTECT)
    is_main = models.BooleanField()

    def __str__(self):
        return f"{self.item.name} - {self.color.name}"


class Image(models.Model):
    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"

    image = models.ImageField(upload_to='item', blank=True, null=True)


class ItemColorImage(models.Model):
    itemcolor = models.ForeignKey(ItemColor, related_name="image", on_delete=models.PROTECT)
    image = models.ForeignKey(Image, on_delete=models.PROTECT)
    is_main = models.BooleanField()
