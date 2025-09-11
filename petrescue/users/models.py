from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

# The User model extends Django's built-in AbstractUser to add custom fields.
# We're adding fields like phone_no, pincode, gender, city, state, and date.
class User(AbstractUser):
    """
    Custom User model to store user-related data.
    """
    email = models.EmailField(unique=True, null=False, blank=False)
    phone_no = models.CharField(max_length=20, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return self.username
