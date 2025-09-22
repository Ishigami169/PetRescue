# In pets/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PetViewSet, PetRequestFormView # <-- Import the new view

# The router automatically generates all the URLs for the standard PetViewSet
router = DefaultRouter()
router.register(r'pets', PetViewSet, basename='pet')

urlpatterns = [
    # Add this new URL for your form
    path('pet-request-form/', PetRequestFormView.as_view(), name='pet-request-form'),
    
    # Your existing router URLs for standard pet CRUD
    path('', include(router.urls)),
]