from rest_framework.permissions import BasePermission


class IsOwnProfile(BasePermission):
    """Allows write access only to the own profile."""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user