from django.db import models
from django.utils.translation import gettext_lazy as _


class EmailTemplate(models.Model):
    class Meta:
        verbose_name = _("Шаблон")
        verbose_name_plural = _("Шаблоны")

    id = models.CharField(max_length=20, primary_key=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    template = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.id}: {self.description}"


class EmailReceivers(models.Model):
    class Meta:
        verbose_name = _("Получатели")
        verbose_name_plural = _("Получатели")

    id = models.CharField(max_length=20, primary_key=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    template = models.ForeignKey(EmailTemplate, related_name="receivers", on_delete=models.CASCADE)
    email_list = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.id}: {self.description}"
