from rest_framework import serializers

from profiles_app.models import UserProfile


class ProfileUserSerializer(serializers.Serializer):
    """Serializes user data for profile lists."""

    pk = serializers.IntegerField(source="id")
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    file = serializers.ImageField(source="profile.file", read_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a single user profile."""

    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")

    class Meta:
        model = UserProfile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "email",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
            "created_at",
        ]
        read_only_fields = ["user", "username", "type", "created_at"]

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        user = instance.user

        for attr, value in user_data.items():
            setattr(user, attr, value)

        user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class ProfileListSerializer(serializers.ModelSerializer):
    """Serializes profile lists in the API documentation format."""

    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    uploaded_at = serializers.DateTimeField(source="created_at", read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "uploaded_at",
            "type",
        ]