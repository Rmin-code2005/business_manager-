from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager
from .validators import validate_iran_phone


class CustomUser(AbstractUser):

    class GenderChoices(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"
        OTHER = "other", "Other"

    username = None

    email = models.EmailField(
        unique=True,
        blank=False,
        null=False,
    )

    phone = models.CharField(
        max_length=11,
        unique=True,
        validators=[validate_iran_phone],
    )

    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
        blank=True,
        null=True,
    )

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = [
        "phone",
        "first_name",
        "last_name",
    ]

    objects = CustomUserManager()

    def __str__(self):
        return self.email