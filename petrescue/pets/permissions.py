# In pets/permissions.py

from rest_framework import permissions

class IsCreatorOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow creators of an object or admins to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any authenticated user.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the creator of the pet or an admin.
        return obj.created_by == request.user or request.user.is_staff

# --- ADD THIS NEW CLASS ---
class IsReceiverOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow the receiver of a notification or an admin to see/edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Allow the action if the request user is the receiver or if the user is an admin.
        return obj.receiver == request.user or request.user.is_staff