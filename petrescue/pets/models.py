from django.db import models
from django.conf import settings
from core.models import BaseModel

# PetType is a simple lookup table and doesn't need BaseModel inheritance.
class PetType(models.Model):
    type = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.type

# All the models below now inherit from BaseModel
class Pet(BaseModel):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    name = models.CharField(max_length=100)
    pet_type = models.ForeignKey(PetType, on_delete=models.SET_NULL, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    breed = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    image = models.ImageField(upload_to="pets/", null=True, blank=True)
    is_diseased = models.BooleanField(default=False)
    is_vaccinated = models.BooleanField(default=False)


    def __str__(self):
        return self.name


class PetMedicalHistory(BaseModel):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="medical_histories")
    last_vaccinated_date = models.DateField(null=True, blank=True)
    vaccination_name = models.CharField(max_length=100, null=True, blank=True)
    disease_name = models.CharField(max_length=100, null=True, blank=True)
    stage = models.IntegerField(null=True, blank=True)
    no_of_years = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.pet.name} - {self.disease_name or 'Healthy'}"


class PetReport(BaseModel):
    PET_STATUS_CHOICES = [
        ('Lost', 'Lost'),
        ('Found', 'Found'),
        ('Adopted', 'Adopted'),
    ]
    REPORT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Resolved', 'Resolved'),
        ('Reunited', 'Reunited'),
    ]

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="reports")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="pet_reports")
    pet_status = models.CharField(max_length=20, choices=PET_STATUS_CHOICES)
    report_status = models.CharField(max_length=20, choices=REPORT_STATUS_CHOICES, default="Pending")
    image = models.ImageField(upload_to="reports/", null=True, blank=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.pet.name} - {self.pet_status}"


class PetAdoption(BaseModel):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="adoptions")
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="adoption_requests")
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")

    def __str__(self):
        return f"{self.pet.name} adoption - {self.requester}"


class Notification(BaseModel):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_notifications")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_notifications")
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="notifications", null=True, blank=True)
    content = models.TextField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification from {self.sender} to {self.receiver}"