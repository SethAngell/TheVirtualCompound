from django.conf import settings
from django.db import models

# Create your models here.


class Design(models.Model):
    template_name = models.CharField(max_length=150)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class LandingPage(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    bio = models.TextField()
    headline = models.CharField(max_length=100)
    avatar = models.ImageField()
    contact_email = models.EmailField(null=True, blank=True)
    resume = models.FileField(null=True, blank=True)
    template = models.ForeignKey(
        Design, on_delete=models.DO_NOTHING, blank=True, null=True
    )

    def __str__(self):
        return self.name


class Experience(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exp_id = models.AutoField(primary_key=True)
    company = models.CharField(max_length=40)
    title = models.CharField(max_length=65)
    description = models.TextField(blank=True, null=True)
    present = models.BooleanField()
    start_year = models.IntegerField()
    end_year = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.company
