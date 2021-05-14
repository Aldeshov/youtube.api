from rest_framework import serializers

from applications.models import Channel


class ChannelSerializer(serializers.Serializer):
    code = serializers.CharField(read_only=True)
    name = serializers.CharField(min_length=2)
    avatar = serializers.ImageField(allow_null=True)
    is_verified = serializers.BooleanField(read_only=True)
    description = serializers.CharField(allow_null=True, allow_blank=True)
    created_date = serializers.DateTimeField(read_only=True)
    subscribers = serializers.ReadOnlyField()

    def validate_is_verified(self, value):
        if value is True and self.subscribers < 100000:
            raise serializers.ValidationError('To verify Channel need at least 100K subscribers')
        return value

    def create(self, validated_data):
        validated_data.setdefault('owner', self.context.get('user'))
        return Channel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        instance.description = validated_data.get('description')
        instance.avatar = validated_data.get('avatar')
        instance.save()
        return instance
