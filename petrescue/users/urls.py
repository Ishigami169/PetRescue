# In users/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from .views import UserViewSet, PasswordResetRequestView ,PasswordResetConfirmView # <-- Import the new view


router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('', include(router.urls)),
]