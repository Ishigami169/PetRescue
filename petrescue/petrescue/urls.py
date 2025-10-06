# In petrescue/urls.py (This file is already correct)

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/pets/', include('pets.urls')), # This line correctly includes the pets app
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/dashboard/', include('dashboard.urls')), 
    path('api/feedback/', include('feedback.urls')), # <-- ADD THIS LINE

    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]