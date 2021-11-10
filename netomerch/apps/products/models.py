from django.db import models
from django.db.models.deletion import SET_DEFAULT

from config.settings import MEDIA_ROOT

# up-level Category


class Category(models.Model):
    parent_id = models.ForeignKey('self', db_column='parent_id', to_field='id',
                                  on_delete=models.SET_DEFAULT, default=0,)
    category_name = models.TextField(max_length=255, null=False, default='')  # name of the category
    # short description, up to 10 words
    short_description = models.TextField(max_length=255)
    # description of the category
    description = models.TextField(max_length=255)
    # link to the image (path to the hosting''s file or URI)
    image = models.ImageField(upload_to=MEDIA_ROOT)

    def __str__(self):
        return f"{self.id}: parent {self.parent_id}, name {self.category_name}"


#
# Item's level

class Item(models.Model):
    category_id = models.ForeignKey(Category, db_column='category_id',
                                    default=0, on_delete=SET_DEFAULT)  # reference to the product
    default_price = models.DecimalField(max_digits=13, decimal_places=2, default=0.00)  # default price
    item_name = models.TextField(max_length=255, null=False, default='')  # name of the item
    short_description = models.TextField(max_length=255)  # short description, up to 10 words
    description = models.TextField(max_length=255)  # description of the item
    image = models.ImageField(upload_to=MEDIA_ROOT)

    def __str__(self):
        return f"{self.id}: Category {self.category_id}, name {self.category_name}"


class SpecProperty(models.Model):
    # name of the special property
    property_name = models.TextField(max_length=255)
    # description of the special property (for example, for hint in the admin board)
    description = models.TextField(max_length=255)

    def __str__(self):
        return f"{self.id}: property {self.property_name}"


class ItemSpecProperty(models.Model):
    # reference to refbook of special properties
    spec_property_id = models.ForeignKey(
        SpecProperty, db_column='special_property_id', default=0, on_delete=SET_DEFAULT)
    item_id = models.ForeignKey(Item, db_column='item_id', default=0, on_delete=SET_DEFAULT)  # reference to items
    d_value = models.DateTimeField()  # value for d type property
    s_value = models.TextField(max_length=255)  # value for s type property
    n_value = models.DecimalField(max_digits=23, decimal_places=10)  # value for n type property
    text_value = models.TextField(max_length=255)  # text equivalent for property

    def __str__(self):
        return f"{self.id}: item {self.item_id} property {self.spec_property_id} - {self.text_value}"
