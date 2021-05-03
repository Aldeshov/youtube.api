from rest_framework import serializers

from applications.models import Channel
from authentication.serializers import BaseUserSerializer
from tools.random_strings import random_code


class ChannelSerializer(serializers.Serializer):
    code = serializers.CharField(read_only=True)
    owner = BaseUserSerializer(read_only=True)
    name = serializers.CharField()
    avatar = serializers.ImageField(allow_null=True)
    is_verified = serializers.BooleanField(read_only=True)
    description = serializers.CharField(allow_null=True, allow_blank=True)
    subscribers = serializers.IntegerField(read_only=True)
    created_date = serializers.DateTimeField(read_only=True)

    def validate_name(self, value):
        if value == '' and self.owner.full_name != '':
            return self.owner.full_name
        if len(value) < 4:
            raise serializers.ValidationError('Name length has to be more than 4!')
        return value

    def create(self, validated_data):
        validated_data.setdefault('owner', self.context.get('user'))
        validated_data.setdefault('code', random_code())
        return Channel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        instance.description = validated_data.get('description')
        instance.avatar = validated_data.get('avatar')
        instance.save()
        return instance
