# In pets/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PetViewSet

# The router automatically generates all the URLs for the PetViewSet
router = DefaultRouter()
router.register(r'', PetViewSet, basename='pet') # Registers endpoints like /api/pets/ and /api/pets/1/

urlpatterns = [
    path('', include(router.urls)),
]