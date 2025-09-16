# In pets/views.py

from rest_framework import viewsets, permissions
from .models import Pet
from .serializers import PetSerializer

class PetViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing pet instances.
    """
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticated] # Ensures only logged-in users can access

    def perform_create(self, serializer):
        """
        Assign the current user to the created_by field.
        """
        serializer.save(created_by=self.request.user)