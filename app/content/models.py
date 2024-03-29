from accounts.models import CustomUser
from django.db import models


def image_upload_location(instance, filename):
    return f"content/{instance.user.id}/images/{filename}"


def document_upload_location(instance, filename):
    return f"content/{instance.user.id}/documents/{filename}"


class UserImage(models.Model):
    name = models.CharField(max_length=128)
    alt_text = models.CharField(max_length=512)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_upload_location, null=False, blank=True)

    def __str__(self):
        return f"{self.user} - {self.name}"


class UserDocument(models.Model):
    name = models.CharField(max_length=128)
    downloadable = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    file = models.FileField(upload_to=document_upload_location, null=False, blank=True)

    def __str__(self):
        return f"{self.user} - {self.name}"
