from rest_framework.permissions import BasePermission

from profiles_app.models import UserProfile

class IsBusinessUser(BasePermission):
    """Allows only business users."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and UserProfile.objects.filter(
                user=request.user,
                type=UserProfile.BUSINESS,
            ).exists()
        )

class IsOfferCreator(BasePermission):
    """Allows only the offer creator."""

    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user