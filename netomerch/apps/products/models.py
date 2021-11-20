from django.db import models
from django.db.models import JSONField
from taggit.managers import TaggableManager
from django.utils.translation import gettext_lazy as _

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


#
# Item's level


class ItemJSON(models.Model):
    class Meta:
        verbose_name_plural = _("Items")

    category = models.ManyToManyField(Category)
    default_price = models.DecimalField(max_digits=13, decimal_places=2, default=0.00)
    item_name = models.TextField(max_length=255, null=False, default='')
    short_description = models.TextField(max_length=255, blank=True, null=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='item')
    is_published = models.BooleanField(default=False)

    tags = TaggableManager(blank=True)
    properties = JSONField()

    def __str__(self):
        return f"{self.id}: name {self.item_name}"


class SpecProperty(models.Model):
    class Meta:
        verbose_name = "Special property"
        verbose_name_plural = "Special Properties"

    property_name = models.TextField(max_length=255)
    description = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.id}: property {self.property_name}"
