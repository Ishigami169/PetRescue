# In pets/views.py

from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets, permissions, status
from rest_framework.response import Response
from .models import Pet, PetMedicalHistory, PetReport, Notification
from .serializers import PetSerializer, PetRequestSerializer

User = get_user_model()

# This is your existing ViewSet for standard CRUD
class PetViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing pet instances.
    """
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Assign the current user to the created_by field.
        """
        serializer.save(created_by=self.request.user)

# This is the new View for the complex form
class PetRequestFormView(generics.CreateAPIView):
    """
    A view to handle the complete Lost/Found/Adopt pet request form.
    """
    serializer_class = PetRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        medical_data = validated_data.pop('medical_history')
        report_data = validated_data.pop('report')

        pet = Pet.objects.create(**validated_data, created_by=request.user)
        PetMedicalHistory.objects.create(pet=pet, **medical_data, created_by=request.user)
        pet_report = PetReport.objects.create(pet=pet, user=request.user, **report_data, created_by=request.user)

        admin_user = User.objects.filter(is_staff=True).first()
        notification = None
        if admin_user:
            notification = Notification.objects.create(
                sender=request.user,
                receiver=admin_user,
                pet=pet,
                content=f"New pet report '{report_data['pet_status']}' submitted for {pet.name} by {request.user.username}."
            )
        
        response_data = {
            "message": f"{report_data['pet_status']} pet request submitted successfully",
            "pet_id": pet.id,
            "report_id": pet_report.id,
            "notification_id": notification.id if notification else None
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)