from django.db import models
from django.db.models.deletion import SET_DEFAULT
from taggit.managers import TaggableManager

from config.settings import MEDIA_ROOT

# up-level Category


class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"

    category_name = models.TextField(max_length=255, null=False, default='')
    short_description = models.TextField(max_length=255, null=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='images')

    tags = TaggableManager(blank=True)

    def __str__(self):
        return f"{self.id}: name {self.category_name}"


#
# Item's level

class Item(models.Model):
    category_id = models.ForeignKey(Category, db_column='category_id',
                                    default=0, on_delete=SET_DEFAULT)
    default_price = models.DecimalField(max_digits=13, decimal_places=2, default=0.00)
    item_name = models.TextField(max_length=255, null=False, default='')
    short_description = models.TextField(max_length=255, blank=True, null=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='images')
    is_published = models.BooleanField(default=False)

    tags = TaggableManager(blank=True)

    def __str__(self):
        return f"{self.id}: Category {self.category_id}, name {self.item_name}"


class SpecProperty(models.Model):
    class Meta:
        verbose_name = "Special property"
        verbose_name_plural = "Special Properties"

    property_name = models.TextField(max_length=255)
    description = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.id}: property {self.property_name}"


class ItemSpecProperty(models.Model):
    class Meta:
        verbose_name = "Setting item's special property"
        verbose_name_plural = "Setting item's special properties"
        constraints = [
            models.UniqueConstraint(fields=['spec_property_id', 'item_id'], name='unique item_prop')
        ]
    spec_property_id = models.ForeignKey(
        SpecProperty, db_column='special_property_id', default=0, on_delete=SET_DEFAULT)
    item_id = models.ForeignKey(Item, db_column='item_id', default=0, on_delete=SET_DEFAULT)
    d_value = models.DateTimeField(blank=True, null=True)
    s_value = models.TextField(max_length=255, blank=True, null=True)
    n_value = models.DecimalField(max_digits=23, decimal_places=10, blank=True, null=True)
    text_value = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.id}: item {self.item_id} property {self.spec_property_id} - {self.text_value}"
