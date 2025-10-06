# In feedback/views.py

from rest_framework import viewsets, permissions
from .models import UserStory
from .serializers import UserStorySerializer, UserStoryCreateSerializer

class UserStoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and creating user stories.
    """
    queryset = UserStory.objects.all().order_by('-created_date')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        # Use a different serializer for 'create' action vs. 'list'/'retrieve'
        if self.action == 'create':
            return UserStoryCreateSerializer
        return UserStorySerializer

    def perform_create(self, serializer):
        # Automatically set the logged-in user when a new story is created
        serializer.save(user=self.request.user)