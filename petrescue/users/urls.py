from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token # <-- IMPORT THIS

from .views import UserRegistrationView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', obtain_auth_token, name='user-login'), # <-- ADD THIS LINE

]