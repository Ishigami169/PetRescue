from rest_framework import serializers
from .models import Pet, PetType

class PetSerializer(serializers.ModelSerializer):
    # This is the key change.
    # It tells DRF to use the 'type' field from the PetType model
    # for reading and writing, instead of the ID.
    pet_type = serializers.SlugRelatedField(
        queryset=PetType.objects.all(),
        slug_field='type'
    )

    class Meta:
        model = Pet
        # List all the fields from your Pet model that you want in your API
        fields = [
            'id', 'name', 'pet_type', 'gender', 'breed', 'color', 'age',
            'weight', 'description', 'address', 'state', 'city', 'pincode',
            'image', 'is_diseased', 'is_vaccinated'
        ]