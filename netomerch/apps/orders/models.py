from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from ..products.models import Item


class Order(models.Model):
    class Status(models.enums.Choices):
        NEW = _('NEW')
        IN_PROGRESS = _('IN PROGRESS')
        DONE = _('DONE')

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    name = models.CharField(max_length=50, null=False, verbose_name=_('Buyer name'))
    email = models.CharField(max_length=100, null=False, verbose_name=_('Buyer email'))
    phone = PhoneNumberField(null=False)
    promo = models.CharField(max_length=50, blank=True, null=True)
    items = models.ManyToManyField(Item, through='ItemConnections', related_name='orders')
    status = models.CharField(max_length=15, choices=Status.choices, verbose_name=_('status'), default=Status.NEW)

class ItemConnections(models.Model):
    orders = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='item')
    items = models.ForeignKey(Item, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
