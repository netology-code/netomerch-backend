from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import SET_DEFAULT

# Create your models here.


class Address(models.Model):
    address = models.TextField()

    def __str__(self):
        return self.address


class Customer(AbstractUser):
    uid = models.TextField(max_length=100)
    phone = models.TextField(max_length=255)
    addresses = models.ManyToManyField(Address)
    ip = models.TextField(max_length=255)
    is_registered = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
