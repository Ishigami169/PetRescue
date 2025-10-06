# In pets/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
# Import the new PetReportViewSet
from .views import PetViewSet, PetRequestFormView, NotificationViewSet, PetAdoptionViewSet, PetReportViewSet

router = DefaultRouter()
router.register(r'pets', PetViewSet, basename='pet')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'adoptions', PetAdoptionViewSet, basename='adoption')
# --- ADD THIS NEW LINE ---
router.register(r'reports', PetReportViewSet, basename='report')

urlpatterns = [
    path('pet-request-form/', PetRequestFormView.as_view(), name='pet-request-form'),
    path('', include(router.urls)),
]