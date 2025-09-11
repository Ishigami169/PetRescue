from django.db import models

# Create your models here.
from django.conf import settings

# This is the Pet model, which contains information about the animals.
# It includes fields for breed, color, location, and a status indicating
# if the pet is vaccinated or diseased.
class Pet(models.Model):
    """
    Model to store pet-related data.
    """
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    colour = models.CharField(max_length=50)
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='pet_images/', null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    is_vaccinated = models.BooleanField(default=False)
    is_diseased = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pets')

    def __str__(self):
        return self.name

# The PetMedicalHistory model stores medical records for each pet.
# It has a foreign key to the Pet model.
class PetMedicalHistory(models.Model):
    """
    Model to store medical history for a pet.
    """
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='medical_history')
    vaccine_name = models.CharField(max_length=100, null=True, blank=True)
    last_vaccinated_date = models.DateField(null=True, blank=True)
    stage = models.CharField(max_length=100, null=True, blank=True)
    treatment_name = models.CharField(max_length=100, null=True, blank=True)
    disease_name = models.CharField(max_length=100, null=True, blank=True)
    no_of_years = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Medical history for {self.pet.name}"

# The PetReport model is for reporting a pet's status (lost, found, or adoptable).
class PetReport(models.Model):
    """
    Model to store reports about a pet.
    """
    REPORT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Reunited', 'Reunited'),
        ('Lost', 'Lost'),
        ('Found', 'Found'),
        ('Adopt', 'Adopt'),
    ]
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='reports')
    status = models.CharField(max_length=20, choices=REPORT_STATUS_CHOICES, default='Pending')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reported_pets')
    image = models.ImageField(upload_to='report_images/', null=True, blank=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Report for {self.pet.name} - {self.get_status_display()}"

# The PetAdoption model tracks adoption requests.
class PetAdoption(models.Model):
    """
    Model to track pet adoption requests.
    """
    ADOPTION_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='adoptions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='adoption_requests')
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=ADOPTION_STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Adoption request for {self.pet.name} by {self.user.username}"

# The Notification model handles in-app notifications.
class Notification(models.Model):
    """
    Model to store notifications.
    """
    message = models.TextField()
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_notifications')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_notifications')
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.receiver.username}"
