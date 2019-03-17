from django.db import models
from django.contrib.auth.models import AbstractUser
from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin
from django.dispatch import receiver
from django.db.models.signals import post_save

class User(SimpleEmailConfirmationUserMixin, AbstractUser):
    pass

class Registration(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    publicKey = models.TextField()
    privateKey = models.TextField(blank=True, null=True)