# In users/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom User model strictly following the document's specifications.
    """
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    # Fields from the document
    email = models.EmailField(unique=True) # [cite: 9]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True) # 
    phone_no = models.CharField(max_length=20, null=True, blank=True) # [cite: 12]
    address = models.TextField(null=True, blank=True) # 
    pincode = models.BigIntegerField(null=True, blank=True) # 
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True) # [cite: 15]

    # Username and Password fields are handled by AbstractUser [cite: 8, 10]

    def __str__(self):
        return self.username