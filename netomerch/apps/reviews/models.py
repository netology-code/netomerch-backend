from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.orders.models import ItemConnections

# Create your models here.


class Review(models.Model):
    """ description: Review """

    class Meta:
        verbose_name_plural = _("Reviews")

    orders_item = models.ForeignKey(ItemConnections, blank=False, on_delete=models.CASCADE, related_name='reviews')
    author = models.CharField(max_length=100, blank=False, null=False, default='Anonymous')
    email = models.EmailField(null=False, blank=False)
    text = models.TextField(blank=False, null=False, default='')
    is_published = models.BooleanField(default=False, blank=False, null=False)

    def __str__(self):
        return f"review {self.id}"
