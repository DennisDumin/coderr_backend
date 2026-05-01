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


class IsCustomerUser(BasePermission):
    """Allows only customer users."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and UserProfile.objects.filter(
                user=request.user,
                type=UserProfile.CUSTOMER,
            ).exists()
        )