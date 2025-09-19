# In users/views.py

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from .permissions import IsOwnerOrAdmin # <-- Import the correct permission

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Return the authenticated user's data.
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        """
        Assigns permissions based on the action.
        """
        if self.action == 'create':
            self.permission_classes = [permissions.AllowAny]
        elif self.action == 'list':
            self.permission_classes = [permissions.IsAdminUser]
        elif self.action == 'me':
            self.permission_classes = [permissions.IsAuthenticated]
        else: # This applies to 'retrieve', 'update', 'partial_update', 'destroy'
            self.permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
        return super().get_permissions()