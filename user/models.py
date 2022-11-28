from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone = models.IntegerField(default=10)
    location = models.CharField(max_length=200)