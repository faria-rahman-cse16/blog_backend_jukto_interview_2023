from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsModeratorOrReadOnly(BasePermission):
    """
    Custom permission to allow moderators to modify an object, but only allow
    read-only access to non-moderators.
    """
    def has_permission(self, request, view):
        """
        Return True if the user making the request is a moderator or if the request
        is safe (i.e., a read-only request), otherwise return False.
        """
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_moderator

    def has_object_permission(self, request, view, obj):
        """
        Return True if the user making the request is a moderator or if the request
        is safe (i.e., a read-only request) and False otherwise.
        """
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_moderator