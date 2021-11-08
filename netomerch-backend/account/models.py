from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import SET_DEFAULT

# Create your models here.


class Customer(AbstractUser):
    uid = models.TextField(max_length=100)
    phone = models.TextField(max_length=255)
    address = models.TextField(blank=True)
    ip = models.TextField(max_length=255)
    is_registered = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username}: {self.first_name} {self.last_name} {self.email}"
