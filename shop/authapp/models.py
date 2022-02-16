from time import time
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.forms import ValidationError
from django.utils.timezone import now

from datetime import timedelta


def get_expiration_time():
    return now() + timedelta(hours=48)


class ShopUser(AbstractUser):
    age = models.PositiveIntegerField(verbose_name="Age")
    image = models.ImageField(verbose_name="User image", blank=True, upload_to="users")
    phone = models.CharField(
        verbose_name="Phone number",
        max_length=20,
        blank=True,
        validators=[
            RegexValidator(
                r"\d-\d{3}-\d{3}-\d{4}$",
                message="Phone must be in *-***-***-**** format.",
            )
        ],
    )
    city = models.CharField(verbose_name="City", max_length=30, blank=True)
    activation_key = models.CharField(max_length=128, blank=True)
    key_expires = models.DateTimeField(default=get_expiration_time())

    def clean(self):
        if self.age > 100:
            raise ValidationError(
                {
                    "age": f"Seriosly, age {self.age}?\
                    Must be under 100, or i don't pass you."
                }
            )
