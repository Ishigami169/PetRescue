from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Pet
from .serializers import PetSerializer
from .permissions import IsOwnerOrReadOnly # <-- Import the custom permission

class PetListCreateView(generics.ListCreateAPIView):
    """
    API view to list all pets or create a new pet.
    """
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# This new view handles Retrieve (GET one), Update (PUT/PATCH), and Destroy (DELETE)
class PetDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a single pet instance.
    """
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [IsOwnerOrReadOnly] # <-- Use the custom permission

