from django.contrib import admin
from .models import (
    PetType,
    Pet,
    PetMedicalHistory,
    PetReport,
    PetAdoption,
    Notification
)

# Register your models here.
admin.site.register(PetType)
admin.site.register(Pet)
admin.site.register(PetMedicalHistory)
admin.site.register(PetReport)
admin.site.register(PetAdoption)
admin.site.register(Notification)