from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    name = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    gender = models.CharField(
        max_length=100,
        choices=GenderChoices.choices,
    )
    avatar = models.URLField(blank=True)
    is_host = models.BooleanField(default=False)
    is_custom = models.BooleanField(default=False)
    is_realtor = models.BooleanField(default=False)
