

# Create your views here.
# In dashboard/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth import get_user_model
from pets.models import PetReport, PetAdoption

User = get_user_model()

class AdminDashboardMetricsView(APIView):
    """
    An API view that provides aggregated metrics for the admin dashboard.
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        # Calculate all the required metrics
        total_pets_reported = PetReport.objects.count()
        total_adoptions_approved = PetAdoption.objects.filter(status='Approved').count()
        total_lost_pets = PetReport.objects.filter(pet_status='Lost').count()
        total_found_pets = PetReport.objects.filter(pet_status='Found').count()
        total_registered_users = User.objects.count()
        total_cases_resolved = PetReport.objects.filter(report_status='Resolved').count()

        # Assemble the data into a dictionary
        data = {
            'total_pets_reported': total_pets_reported,
            'total_adoptions_approved': total_adoptions_approved,
            'lost_vs_found_stats': {
                'lost': total_lost_pets,
                'found': total_found_pets,
            },
            'total_registered_users': total_registered_users,
            'total_cases_resolved': total_cases_resolved,
        }

        return Response(data)