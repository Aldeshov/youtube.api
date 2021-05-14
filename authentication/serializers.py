from rest_framework import serializers

from authentication.models import User

NOT_ALLOWED_PASSWORDS = ['password', '12345678', 'qwertyuiop', '11111111', '00000000', 'asdfghjk', ]


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
    password = serializers.CharField(write_only=True, min_length=8, max_length=16)

    @classmethod
    def validate_password(cls, value):
        if value in NOT_ALLOWED_PASSWORDS:
            raise serializers.ValidationError('Password is too insecure, use another')
        return value

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
