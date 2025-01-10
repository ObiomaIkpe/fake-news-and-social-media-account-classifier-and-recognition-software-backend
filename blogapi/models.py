from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    is_fake = models.BooleanField(default=False)
    fake_count = models.IntegerField(default=0)
    profile_picture = models.ImageField(upload_to="profile_img", blank=True, null=True)

    def __str__(self):
        return self.username
