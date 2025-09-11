from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import User
from .serializers import UserRegistrationSerializer

class UserRegistrationView(generics.CreateAPIView):
    """
    API view to create a new user.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer