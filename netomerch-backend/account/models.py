from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import SET_DEFAULT

# Create your models here.


class Address(models.Model):
    country = models.TextField(max_length=100, blank=True)
    region = models.TextField(max_length=100, blank=True)
    city = models.TextField(max_length=100, blank=True)
    street = models.TextField(max_length=100, blank=True)
    house = models.TextField(max_length=10, blank=True)
    appartment = models.TextField(max_length=10, blank=True)
    extra_info = models.TextField(max_length=255, blank=True)

    address = models.TextField(blank=True)

    def __str__(self):
        return self.address


class Customer(AbstractUser):
    uid = models.TextField(max_length=100)
    phone = models.TextField(max_length=255)
    addresses = models.ManyToManyField(Address, blank=True)
    ip = models.TextField(max_length=255)
    is_registered = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.email}"
