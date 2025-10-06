# In pets/views.py

from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
# --- MAKE SURE ALL MODELS ARE IMPORTED ---
from .models import Pet, PetAdoption, PetMedicalHistory, PetReport, Notification
from .serializers import (
    PetSerializer, PetRequestSerializer, NotificationSerializer,
    # --- IMPORT THE TWO NEW SERIALIZERS ---
    PetAdoptionSerializer, PetReportUpdateSerializer
)
from .permissions import IsCreatorOrAdmin, IsReceiverOrAdmin

User = get_user_model()

class PetViewSet(viewsets.ModelViewSet):
    # ... (Your existing PetViewSet code remains here) ...
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticated, IsCreatorOrAdmin]
    def get_queryset(self):
        queryset = Pet.objects.all()
        tab = self.request.query_params.get('tab', None)
        if tab:
            if tab == 'lost':
                return queryset.filter(reports__pet_status='Lost', reports__report_status='Accepted').distinct()
            elif tab == 'found':
                return queryset.filter(reports__pet_status='Found', reports__report_status='Accepted').distinct()
            elif tab == 'adopt':
                return queryset.filter(reports__pet_status='Adopted', reports__report_status='Accepted').distinct()
        return queryset
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class PetRequestFormView(generics.CreateAPIView):
    # ... (Your existing PetRequestFormView code remains here) ...
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
                sender=request.user, receiver=admin_user, pet=pet,
                content=f"New pet report '{report_data['pet_status']}' submitted for {pet.name} by {request.user.username}."
            )
        response_data = {
            "message": f"{report_data['pet_status']} pet request submitted successfully",
            "pet_id": pet.id, "report_id": pet_report.id,
            "notification_id": notification.id if notification else None
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

class NotificationViewSet(viewsets.ModelViewSet):
    # ... (Your existing NotificationViewSet code remains here) ...
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated, IsReceiverOrAdmin]
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Notification.objects.all().order_by('-created_date')
        return Notification.objects.filter(receiver=user).order_by('-created_date')

# --- ADD THESE TWO NEW VIEWSETS AT THE BOTTOM ---

class PetAdoptionViewSet(viewsets.ModelViewSet):
    """
    A viewset for creating and viewing pet adoption requests.
    """
    serializer_class = PetAdoptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return PetAdoption.objects.all()
        return PetAdoption.objects.filter(requester=user)

    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)

class PetReportViewSet(viewsets.ModelViewSet):
    """
    A viewset for Admins to manage Pet Reports.
    """
    queryset = PetReport.objects.all()
    serializer_class = PetReportUpdateSerializer
    permission_classes = [permissions.IsAdminUser]