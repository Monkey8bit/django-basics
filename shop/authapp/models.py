from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.forms import ValidationError
from django.utils.timezone import now

from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver


def get_expiration_time():
    return now() + timedelta(hours=48)


class ShopUser(AbstractUser):
    age = models.PositiveIntegerField(verbose_name="Age", default=18)
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
    key_expires = models.DateTimeField(default=get_expiration_time)

    def clean(self):
        if self.age > 100:
            raise ValidationError(
                {
                    "age": f"Seriosly, age {self.age}?\
                    Must be under 100, or i don't pass you."
                }
            )


class ShopUserProfile(models.Model):
    MALE = "M"
    FEMALE = "F"
    NON_BINARY = "X"

    GENDERS = (
        (MALE, "Male"),
        (FEMALE, "Female"),
        (NON_BINARY, "Non binary"),
    )

    user = models.OneToOneField(ShopUser, null=False, on_delete=models.CASCADE, db_index=True, related_name="profile")
    about = models.TextField(verbose_name="About", max_length=512, blank=True)
    gender = models.CharField(verbose_name="Gender", choices=GENDERS, max_length=1)


@receiver(post_save, sender=ShopUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ShopUserProfile.objects.create(user=instance)
    else:
        instance.profile.save()
