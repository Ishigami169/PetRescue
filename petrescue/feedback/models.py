
# In feedback/models.py

from django.db import models
from django.conf import settings
from core.models import BaseModel
from pets.models import Pet

class UserStory(BaseModel):
    """
    Model to store user feedback or stories about their pets.
    """
    # Title for the story, which is a useful addition
    title = models.CharField(max_length=200)
    
    # [cite_start]Fields from your document [cite: 124]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='stories')
    pet = models.ForeignKey(Pet, on_delete=models.SET_NULL, null=True, blank=True, related_name='stories')
    content = models.TextField()

    def __str__(self):
        return f"'{self.title}' by {self.user.username}"

    class Meta:
        verbose_name_plural = 'User Stories'