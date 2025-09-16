# In users/views.py

from rest_framework import viewsets, permissions
from .models import User
from .serializers import UserSerializer
from .permissions import IsOwnerOrReadOnly # <-- Import our new permission

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            # Anyone can create a new user (register)
            self.permission_classes = [permissions.AllowAny]
        elif self.action == 'list':
            # Only admin users can see the list of all users
            self.permission_classes = [permissions.IsAdminUser]
        else:
            # For retrieve, update, or delete, the user must be authenticated
            # and can only affect their own account.
            self.permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
        return super().get_permissions()