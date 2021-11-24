from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from ..products.models import Item


class Order(models.Model):

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    name = models.CharField(max_length=50, null=False, verbose_name=_('Buyer name'))
    email = models.CharField(max_length=100, null=False, verbose_name=_('Buyer email'))
    phone = PhoneNumberField(null=False)
    promo = models.CharField(max_length=50, blank=True, null=True)
    items = models.ManyToManyField(Item, related_name='orders')


