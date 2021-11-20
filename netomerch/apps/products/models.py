from django.db import models
from django.db.models import JSONField
from taggit.managers import TaggableManager

# up-level Category


#
# Item's level


class SpecProperty(models.Model):
    class Meta:
        verbose_name = "Special property"
        verbose_name_plural = "Special Properties"

    property_name = models.TextField(max_length=255)
    description = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.id}: property {self.property_name}"


class CategoryJSON(models.Model):
    class Meta:
        verbose_name_plural = "Categories' JSON"

    category_name = models.TextField(max_length=255, null=False, default='')
    short_description = models.TextField(max_length=255, null=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='categoriesjson')
    tags = TaggableManager(blank=True)

    def __str__(self):
        return f"{self.id}: name {self.category_name}"


class ItemJSON(models.Model):
    class Meta:
        verbose_name_plural = "Items' JSON"

    category = models.ManyToManyField(CategoryJSON)
    default_price = models.DecimalField(max_digits=13, decimal_places=2, default=0.00)
    item_name = models.TextField(max_length=255, null=False, default='')
    short_description = models.TextField(max_length=255, blank=True, null=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='itemsjson')
    is_published = models.BooleanField(default=False)

    tags = TaggableManager(blank=True)
    properties = JSONField()

    def __str__(self):
        return f"{self.id}: name {self.item_name}"
