from django.db import models
from django.db.models.deletion import SET_NULL
from django.utils.translation import gettext_lazy as _

from ..orders.models import Order
from ..products.models import Item

# Create your models here.


class Review(models.Model):
    '''

    description: Review

    '''
    class Meta:
        verbose_name_plural = _("Reviews")

    order = models.ForeignKey(Order, on_delete=SET_NULL, null=True)
    item = models.ForeignKey(Item, on_delete=SET_NULL, null=True)
    author = models.CharField(max_length=100, blank=False, null=False, default='Anonymous')
    email = models.EmailField()
    text = models.TextField(blank=False, null=False, default='')
    is_published = models.BooleanField(default=False, blank=False, null=False)

    def __str__(self):
        return f"review {self.id} on f{self.item}"
