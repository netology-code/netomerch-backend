from django.db import models
from django.db.models.deletion import SET_DEFAULT
from django.db.models.fields import IntegerField
from django.utils import timezone

# Create your models here.


class Category(models.Model):
    # parent_id = models.IntegerField()  # link to the parent category, if applicable
    # parent_id = models.ForeignKey(
    #     'self', db_column='parent_id', to_field='id',
    #     on_delete=models.SET_DEFAULT, default=0,)
    category_name = models.TextField(
        max_length=255, null=False, default='')  # name of the category
    # short description, up to 10 words
    short_description = models.TextField(max_length=255)
    # description of the category
    description = models.TextField(max_length=255)
    # link to the image (path to the hosting''s file or URI)
    image = models.TextField(max_length=255)


class Customers(models.Model):
    first_name = models.TextField(max_length=255)
    last_name = models.TextField(max_length=255)
    password = models.TextField(max_length=255)
    phone = models.TextField(max_length=255)
    email = models.TextField(max_length=255)
    address = models.TextField(max_length=255)
    ip = models.TextField(max_length=255)
    is_registered = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


class SpecProperties(models.Model):
    # name of the special property
    property_name = models.TextField(max_length=255)
    # description of the special property (for example, for hint in the admin board)
    description = models.TextField(max_length=255)


class Items(models.Model):
    category_id = models.ForeignKey(Category, db_column='category_id',
                                    default=0, on_delete=SET_DEFAULT)  # reference to the product
    default_price = models.DecimalField(
        max_digits=13, decimal_places=2, default=0.00)  # default price
    item_name = models.TextField(
        max_length=255, null=False, default='')  # name of the item
    # short description, up to 10 words
    short_description = models.TextField(max_length=255)
    description = models.TextField(max_length=255)  # description of the item


class ItemSpecProperties(models.Model):
    special_property_id = models.ForeignKey(
        SpecProperties, db_column='special_property_id', default=0, on_delete=SET_DEFAULT)  # reference to refbook of special properties
    item_id = models.ForeignKey(
        Items, db_column='item_id', default=0, on_delete=SET_DEFAULT)  # reference to items
    d_value = models.DateTimeField()  # value for d type property
    s_value = models.TextField(max_length=255)  # value for s type property
    n_value = models.DecimalField(
        max_digits=23, decimal_places=10)  # value for n type property
    # text equivalent for property
    text_value = models.TextField(max_length=255)


class OrderStates(models.Model):
    # name of an order''s state, for example - paying
    state_name = models.TextField(max_length=255, null=False, default='')
    description = models.TextField(max_length=255)


class Orders(models.Model):
    uid = models.TextField(max_length=100)  # unique identifier of order
    order_created_at = models.DateTimeField(
        null=False, default=timezone.now)  # timestamp of creation an order

    order_finished_at = models.DateTimeField()  # timestamp of finishing an order
    order_state_id = models.ForeignKey(
        OrderStates, db_column='order_state_id', default=0, on_delete=SET_DEFAULT)  # reference to order_state
    # timestamp of the last update of the order
    order_updated_at = models.DateTimeField(
        null=False, default=timezone.now)  # reference to order_state
    discount_program = models.IntegerField()  # field for future feature :)
    customer_id = models.ForeignKey(
        Customers, db_column='customer_id', default=0, on_delete=SET_DEFAULT)  # reference to customers
    # delivery address if applicable
    cust_address = models.TextField(max_length=255)
    # cusomer''s phone if applicable
    cust_phone = models.TextField(max_length=255)
    # customer''s e-mail if applicable
    cust_email = models.TextField(max_length=255)
    # delivery date and time if applicable
    order_delivery_at = models.DateTimeField()
    total_sum = models.DecimalField(
        max_digits=13, decimal_places=2, default=0.00)  # total sum of the order


class OrderContents(models.Model):
    order_id = models.ForeignKey(
        Orders, db_column='order_id', default=0, on_delete=SET_DEFAULT)  # reference to Orders
    item_id = models.ForeignKey(
        Items, db_column='item_id', default=0, on_delete=SET_DEFAULT)  # reference to Orders