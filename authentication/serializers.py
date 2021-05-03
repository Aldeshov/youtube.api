from rest_framework import serializers

from applications.models import Profile
from authentication.models import User


class ProfileSerializer(serializers.ModelSerializer):
    """
    Used for only get Information about User profile.
    For Updating Information use functions in Profile() class.
    """
    is_private = serializers.BooleanField(read_only=True)
    saved_playlists = serializers.ListField(read_only=True)
    saved_contents = serializers.ListField(read_only=True)
    liked = serializers.ListField(read_only=True)
    disliked = serializers.ListField(read_only=True)
    subscribed = serializers.ListField(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'


class BaseUserSerializer(serializers.Serializer):
    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    full_name = serializers.ReadOnlyField()
    avatar = serializers.ImageField(read_only=True)

    def create(self, validated_data):
        """
        This is base Serializer function without any action
        """
        return None

    def update(self, instance, validated_data):
        """
        This is base Serializer function without any action
        """
        return None


class CreateUserSerializer(BaseUserSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        return User.objects.create_user(
            validated_data.get("email"),
            validated_data.get("password"),
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name")
        )


class UpdateUserSerializer(BaseUserSerializer):
    avatar = serializers.ImageField(write_only=True, allow_null=True)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.avatar = validated_data.get('avatar')
        instance.save()
        return instance
