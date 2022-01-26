from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.forms import ValidationError


class ShopUser(AbstractUser):
    age = models.PositiveIntegerField(verbose_name="Age")
    image = models.ImageField(verbose_name="User image", blank=True, upload_to="users")
    phone = models.CharField(
        verbose_name="Phone number",
        max_length=20,
        blank=True,
        validators=[RegexValidator(r'\d-\d{3}-\d{3}-\d{4}$', message='Phone must be in *-***-***-**** format.')])
    city = models.CharField(verbose_name="City", max_length=30, blank=True)

    def clean(self):
        if self.age > 100:
            raise ValidationError({"age": f"Seriosly, age {self.age}?\nMust be under 100, or i don't pass you."})
