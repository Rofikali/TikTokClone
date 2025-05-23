
from django.db import models
# from django.contrib.auth.models import BaseUserManager, AbstractUser


class AutoUpdate(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
