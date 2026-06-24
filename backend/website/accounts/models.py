from django.contrib.auth.models import AbstractUser
from django.db import models
from .validators import validate_iran_phone
from .managers import CustomUserManager
class CustomUser(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True,
        blank=False,
        null=False
    )

    phone = models.CharField(
        max_length=11,
        unique=True,
        validators=[validate_iran_phone]
    )

    USERNAME_FIELD = "email"
    objects = CustomUserManager()
    REQUIRED_FIELDS = [
        "phone",
        "first_name",
        "last_name"
    ]