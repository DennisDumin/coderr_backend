from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from profiles_app.models import UserProfile
from .permissions import IsOwnProfile
from .serializers import ProfileListSerializer, UserProfileSerializer


class UserProfileDetailView(RetrieveUpdateAPIView):
    """Handles retrieving and updating a single user profile."""

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()
    http_method_names = ["get", "patch"]

    def get_object(self):
        user_pk = self.kwargs["pk"]
        profile = get_object_or_404(UserProfile, user__pk=user_pk)
        self.check_object_permissions(self.request, profile)
        return profile

    def get_permissions(self):
        if self.request.method == "PATCH":
            return [IsAuthenticated(), IsOwnProfile()]
        return [IsAuthenticated()]


class BusinessProfileListView(ListAPIView):
    """Returns all business profiles."""

    serializer_class = ProfileListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return UserProfile.objects.filter(type=UserProfile.BUSINESS)


class CustomerProfileListView(ListAPIView):
    """Returns all customer profiles."""

    serializer_class = ProfileListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return UserProfile.objects.filter(type=UserProfile.CUSTOMER)