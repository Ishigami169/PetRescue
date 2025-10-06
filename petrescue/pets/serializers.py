# In pets/serializers.py (Replace the entire file with this)

from rest_framework import serializers
from .models import Pet, PetAdoption, PetType, PetMedicalHistory, PetReport, Notification
from users.serializers import UserSerializer

# --- READ-ONLY Serializers for Nesting in Pet Details ---
class PetMedicalHistoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetMedicalHistory
        fields = '__all__'

class PetReportDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = PetReport
        fields = '__all__'

# --- Main Serializer for Pet CRUD (PetViewSet) ---
class PetSerializer(serializers.ModelSerializer):
    pet_type = serializers.SlugRelatedField(
        queryset=PetType.objects.all(),
        slug_field='type'
    )
    # ADD THESE TWO LINES for nested details
    medical_histories = PetMedicalHistoryDetailSerializer(many=True, read_only=True)
    reports = PetReportDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Pet
        # ADD 'medical_histories' AND 'reports' to the fields list
        fields = [
            'id', 'name', 'pet_type', 'gender', 'breed', 'color', 'age',
            'weight', 'description', 'address', 'state', 'city', 'pincode',
            'image', 'is_diseased', 'is_vaccinated', 'medical_histories', 'reports'
        ]

# --- Serializers for the Custom Pet Request Form ---
class PetMedicalHistoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetMedicalHistory
        fields = '__all__'
class PetReportDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = PetReport
        fields = '__all__'
class PetSerializer(serializers.ModelSerializer):
    pet_type = serializers.SlugRelatedField(queryset=PetType.objects.all(), slug_field='type')
    medical_histories = PetMedicalHistoryDetailSerializer(many=True, read_only=True)
    reports = PetReportDetailSerializer(many=True, read_only=True)
    class Meta:
        model = Pet
        fields = ['id', 'name', 'pet_type', 'gender', 'breed', 'color', 'age', 'weight', 'description', 'address', 'state', 'city', 'pincode', 'image', 'is_diseased', 'is_vaccinated', 'medical_histories', 'reports']
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
    pet_type = serializers.SlugRelatedField(queryset=PetType.objects.all(), slug_field='type')
    class Meta:
        model = Pet
        fields = ['name', 'pet_type', 'gender', 'breed', 'color', 'age', 'weight', 'description', 'address', 'state', 'city', 'pincode', 'image', 'is_diseased', 'is_vaccinated', 'medical_history', 'report']
class NotificationPetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ['id', 'name', 'breed']
class NotificationSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    pet = NotificationPetSerializer(read_only=True)
    class Meta:
        model = Notification
        fields = ['id', 'sender', 'receiver', 'pet', 'content', 'is_read', 'created_date']
class PetReportUpdateSerializer(serializers.ModelSerializer):
    pet = PetSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = PetReport
        fields = ['id', 'pet', 'user', 'pet_status', 'report_status', 'is_resolved', 'created_date']
        read_only_fields = ['id', 'pet', 'user', 'pet_status', 'created_date']

# --- ADD THIS NEW SERIALIZER AT THE BOTTOM ---
class PetAdoptionSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and viewing PetAdoption requests.
    """
    class Meta:
        model = PetAdoption
        fields = ['id', 'pet', 'requester', 'message', 'status', 'created_date']
        # The requester and status are handled automatically by the server,
        # so we make them read-only in the serializer.
        read_only_fields = ['requester', 'status']
