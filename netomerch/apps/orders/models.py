from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from apps.products.models import Item


class Order(models.Model):
    class Status(models.enums.TextChoices):
        NEW = _('Новый')
        IN_PROGRESS = _('В работе')
        DONE = _('Завершен')

    class Meta:
        verbose_name = _("Заказ")
        verbose_name_plural = _("Заказы")

    name = models.CharField(max_length=50, null=False)
    email = models.CharField(max_length=100, null=False)
    phone = PhoneNumberField(null=False)
    item = models.ManyToManyField(Item, through='ItemConnections', related_name='orders')
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.NEW)
    total_sum = models.DecimalField(max_digits=13, decimal_places=2, default=0.00,
                                    blank=False, null=False)
    final_sum = models.DecimalField(max_digits=13, decimal_places=2, default=0.00,
                                    blank=False, null=False)
    create_date = models.DateTimeField(auto_now=True)
    address = models.CharField(max_length=250, null=False)
    comment = models.TextField(blank=True, null=True)
    promocode = models.ForeignKey('Promocode', blank=True, related_name='order', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'Заказ №{self.pk}'


class ItemConnections(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    size = models.CharField(max_length=20)
    color = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=13, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.order.id} - {self.item.name}"


class Promocode(models.Model):

    class Meta:
        verbose_name = _("Промокод")
        verbose_name_plural = _("Промокоды")

    code = models.CharField(primary_key=True, max_length=10, null=False, blank=False)
    email = models.CharField(max_length=100, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)


class PromoUpload(models.Model):
    class Meta:
        verbose_name = "Импорт из xlsx"

    file = models.FileField(upload_to='promo_imports')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    result = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.id}: {self.uploaded_at}"
