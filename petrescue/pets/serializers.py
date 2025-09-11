from rest_framework import serializers
from .models import Pet

class PetSerializer(serializers.ModelSerializer):
    """
    Serializer for the Pet model.
    """
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Pet
        fields = [
            'id', 'name', 'breed', 'type', 'colour', 'location', 
            'age', 'gender', 'description', 'user'
        ]