from rest_framework.permissions import BasePermission

from profiles_app.models import UserProfile


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


class IsReviewCreator(BasePermission):
    """Allows only the review creator."""

    def has_object_permission(self, request, view, obj):
        return obj.reviewer == request.user