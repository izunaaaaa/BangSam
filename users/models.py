from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    name = models.CharField(
        max_length=100,
        unique=True,
    )
    first_name = models.CharField(
        max_length=100,
        editable=False,
    )
    last_name = models.CharField(
        max_length=150,
        editable=False,
    )
    phone_number = models.CharField(
        max_length=11,
        null=True,
    )
    email = models.EmailField(
        max_length=100,
    )
    address = models.CharField(
        max_length=100,
    )
    gender = models.CharField(
        max_length=100,
        choices=GenderChoices.choices,
    )
    avatar = models.URLField(
        blank=True,
        null=True,
    )
    is_host = models.BooleanField(default=False)
    is_realtor = models.BooleanField(default=False)
