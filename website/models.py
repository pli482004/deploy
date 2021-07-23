from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

# Create your models here.


class User(AbstractUser):
    pass


class Bookmark(models.Model):
    title = models.CharField(max_length=64)
    content = models.CharField(max_length=1024, blank=True, null=True)
    link = models.CharField(max_length=256, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")