from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.
class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )
#     username = models.CharField(max_length=200, null=False, unique=True)
#     password = models.CharField(max_length=200, null=False)
#     email = models.CharField(max_length=200, null=False)