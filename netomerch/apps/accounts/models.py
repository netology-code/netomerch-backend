import django.db.models.enums
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Role(django.db.models.enums.Choices):
        MANAGER = 'MANAGER'
        CUSTOMER = 'CUSTOMER'

    role = models.CharField(max_length=10, choices=Role.choices, verbose_name=_('role'))
    # phone = PhoneNumberField()
    # https://github.com/stefanfoulis/django-phonenumber-field#django-phonenumber-field

    def __str__(self):
        return f"{self.username}: {self.first_name} {self.last_name} {self.email}"
