import django.db.models.enums
from django.db import models
from django.db.models import JSONField
from django.db.models.deletion import SET_NULL
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager

# up-level Category


class Category(models.Model):
    class Meta:
        verbose_name_plural = _("Categories")

    name = models.CharField(max_length=50, null=False, default='')
    short_description = models.CharField(max_length=50, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='categories')

    def __str__(self):
        return f"{self.id}: name {self.name}"


class Item(models.Model):
    class Meta:
        verbose_name_plural = _("Items")

    category = models.ManyToManyField(Category)
    price = models.DecimalField(max_digits=13, decimal_places=2, default=0.00, blank=False, null=False)
    name = models.CharField(max_length=50, default='', blank=False, null=False)
    short_description = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ManyToManyField('Image', related_name='items')
    is_published = models.BooleanField(default=False, blank=False, null=False)
    tags = TaggableManager(blank=True)
    properties = JSONField(default=dict)

    def __str__(self):
        return f"{self.id}: name {self.name}"


class Review(models.Model):
    class Meta:
        verbose_name_plural = _("Reviews")

    item = models.ForeignKey(Item, on_delete=SET_NULL, null=True)
    author = models.CharField(max_length=100, blank=False, null=False, default='Anonymous')
    email = models.EmailField()
    text = models.TextField(blank=False, null=False, default='')
    is_published = models.BooleanField(default=False, blank=False, null=False)

    def __str__(self):
        return f"review {self.id} on f{self.item}"


class Image(models.Model):
    class Meta:
        verbose_name_plural = _("Images")

    image = models.ImageField(upload_to='item', blank=True, null=True)
