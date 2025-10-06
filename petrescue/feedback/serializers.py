# In feedback/serializers.py

from rest_framework import serializers
from .models import UserStory
from users.serializers import UserSerializer
from pets.serializers import PetSerializer

class UserStorySerializer(serializers.ModelSerializer):
    """
    Serializer for reading a list of stories.
    """
    user = UserSerializer(read_only=True)
    pet = PetSerializer(read_only=True)

    class Meta:
        model = UserStory
        fields = ['id', 'title', 'content', 'user', 'pet', 'created_date']

class UserStoryCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new story.
    """
    class Meta:
        model = UserStory
        fields = ['title', 'content', 'pet'] # User is set automatically