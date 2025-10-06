# In feedback/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserStoryViewSet

router = DefaultRouter()
router.register(r'stories', UserStoryViewSet, basename='story')

urlpatterns = [
    path('', include(router.urls)),
]