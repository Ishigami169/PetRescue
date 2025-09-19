# In users/permissions.py

from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to interact with it.
    """
    def has_object_permission(self, request, view, obj):
        # The owner of the object or an admin user can perform any action.
        return obj == request.user or request.user.is_staff