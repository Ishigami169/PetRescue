# In pets/serializers.py

from rest_framework import serializers
from .models import Pet, PetType, PetMedicalHistory, PetReport, Notification

# --- Serializer for the standard Pet CRUD (PetViewSet) ---
# This remains the same as your image
class PetSerializer(serializers.ModelSerializer):
    pet_type = serializers.SlugRelatedField(
        queryset=PetType.objects.all(),
        slug_field='type'
    )

    class Meta:
        model = Pet
        fields = [
            'id', 'name', 'pet_type', 'gender', 'breed', 'color', 'age',
            'weight', 'description', 'address', 'state', 'city', 'pincode',
            'image', 'is_diseased', 'is_vaccinated'
        ]

# --- Serializers for the Custom Pet Request Form ---
# These are new classes you need to add
class PetMedicalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PetMedicalHistory
        fields = ['last_vaccinated_date', 'vaccination_name', 'disease_name', 'stage', 'no_of_years']

class PetReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetReport
        fields = ['pet_status', 'image']

class PetRequestSerializer(serializers.ModelSerializer):
    medical_history = PetMedicalHistorySerializer()
    report = PetReportSerializer()
    pet_type = serializers.SlugRelatedField(
        queryset=PetType.objects.all(),
        slug_field='type'
    )

    class Meta:
        model = Pet
        fields = [
            'name', 'pet_type', 'gender', 'breed', 'color', 'age', 'weight',
            'description', 'address', 'state', 'city', 'pincode', 'image',
            'is_diseased', 'is_vaccinated', 'medical_history', 'report'
        ]