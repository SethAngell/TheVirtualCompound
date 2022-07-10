import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    name = models.CharField(max_length=128, default="DoubleL Studio")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.name


class Domain(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Invitation(models.Model):
    email = models.EmailField(_("email address"), unique=True, primary_key=True)
    invitation_code = models.UUIDField(default=uuid.uuid4, editable=False)
    linked_domain = models.ForeignKey(
        Domain, on_delete=models.CASCADE, blank=True, null=True
    )
