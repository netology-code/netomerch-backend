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
    items = models.ManyToManyField(Item, through='ItemConnections', related_name='orders')
    status = models.CharField(max_length=15, choices=Status.choices, verbose_name=_('status'), default=Status.NEW)
    total_sum = models.DecimalField(max_digits=13, decimal_places=2, default=0.00, blank=False, null=False, verbose_name=_('Total sum'))
    final_sum = models.DecimalField(max_digits=13, decimal_places=2, default=0.00, blank=False, null=False, verbose_name=_('Final sum'))
    discount = models.DecimalField(max_digits=13, decimal_places=2, default=0.00, blank=True, null=True, verbose_name=_('Discount'))
    create_date = models.DateTimeField(auto_now=True, verbose_name=_('Create date'))
    address = models.CharField(max_length=250, null=False, verbose_name=_('Address'))
    comment = models.TextField(blank=True, null=True, verbose_name=_('Comment'))



class ItemConnections(models.Model):
    orders = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='item')
    items = models.ForeignKey(Item, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
