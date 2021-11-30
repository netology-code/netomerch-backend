from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Customer(AbstractUser):
    class Role(models.enums.TextChoices):
        MANAGER = 'MANAGER'
        CUSTOMER = 'CUSTOMER'

    role = models.CharField(max_length=10, choices=Role.choices, verbose_name=_('role'), default=Role.CUSTOMER)

    def __str__(self):
        return f"{self.username}: {self.first_name} {self.last_name} {self.email}"
