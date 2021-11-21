from django.db import models
from django.utils.translation import gettext_lazy as _


class EmailTemplate(models.Model):
    class Meta:
        verbose_name_plural = _("Templates")

    id = models.CharField(max_length=20, primary_key=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    template = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.id}: {self.description}"
