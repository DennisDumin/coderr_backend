from django.contrib.auth.models import User
from rest_framework import serializers

from profiles_app.models import UserProfile


class RegistrationSerializer(serializers.Serializer):
    """Validates registration data and creates a user profile."""

    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(choices=UserProfile.TYPE_CHOICES)

    def validate_username(self, value):
        """Validates that the username is unique."""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def validate_email(self, value):
        """Validates that the email is unique."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already taken.")
        return value

    def validate(self, attrs):
        """Validates password confirmation."""
        self._validate_matching_passwords(attrs)
        return attrs

    def create(self, validated_data):
        """Creates a user and profile."""
        profile_type = validated_data.pop("type")
        validated_data.pop("repeated_password")
        user = self._create_user(validated_data)
        self._create_profile(user, profile_type)
        return user

    def _validate_matching_passwords(self, attrs):
        """Checks whether both passwords match."""
        if attrs["password"] != attrs["repeated_password"]:
            raise serializers.ValidationError(
                {"password": "Passwords do not match."}
            )

    def _create_user(self, validated_data):
        """Creates a Django user."""
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

    def _create_profile(self, user, profile_type):
        """Creates the related user profile."""
        UserProfile.objects.create(user=user, type=profile_type)