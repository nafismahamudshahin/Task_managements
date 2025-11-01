from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

"""
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE , primary_key=True , related_name="userprofile")
    image = models.ImageField(upload_to="profile_images", blank=True, default="profile_images/default_profile.jpg")
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
"""

class CustomUser(AbstractUser):
    image = models.ImageField(upload_to="profile_images" , blank=True, default="profile_images/default_profile.jpg")
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.username