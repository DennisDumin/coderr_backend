from rest_framework import serializers

from profiles_app.models import UserProfile
from reviews_app.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """Serializes reviews and validates review rules."""

    class Meta:
        model = Review
        fields = [
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "reviewer",
            "created_at",
            "updated_at",
        ]

    def validate_rating(self, value):
        """Validates that rating is between 1 and 5."""
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate_business_user(self, value):
        """Validates that the reviewed user is a business user."""
        if not self._is_business_user(value):
            raise serializers.ValidationError("Reviewed user must be a business user.")
        return value

    def validate(self, attrs):
        """Validates review creation rules."""
        if self.instance:
            return self._validate_update(attrs)
        self._validate_unique_review(attrs)
        return attrs

    def _validate_update(self, attrs):
        """Allows only rating and description updates."""
        forbidden_fields = set(attrs.keys()) - {"rating", "description"}
        if forbidden_fields:
            raise serializers.ValidationError("Only rating and description can be updated.")
        return attrs

    def _validate_unique_review(self, attrs):
        """Prevents duplicate reviews for one business user."""
        request = self.context["request"]
        business_user = attrs.get("business_user")
        if self._review_exists(request.user, business_user):
            raise serializers.ValidationError(
                {"business_user": "You have already reviewed this business user."}
            )

    def _review_exists(self, reviewer, business_user):
        """Checks whether a review already exists."""
        return Review.objects.filter(
            reviewer=reviewer,
            business_user=business_user,
        ).exists()

    def _is_business_user(self, user):
        """Checks whether a user has a business profile."""
        return UserProfile.objects.filter(
            user=user,
            type=UserProfile.BUSINESS,
        ).exists()