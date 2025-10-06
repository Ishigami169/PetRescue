# In dashboard/urls.py

from django.urls import path
from .views import AdminDashboardMetricsView

urlpatterns = [
    path('metrics/', AdminDashboardMetricsView.as_view(), name='dashboard-metrics'),
]