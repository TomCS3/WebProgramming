from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    # id = models.AutoField(primary_key=True)
    content = models.TextField(blank=True, null=True)

    