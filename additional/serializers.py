from rest_framework import serializers

from additional.models import GameCopyright, SongCopyright, Restrictions
from tools.random_strings import random_key


class AbstractBaseCopyrightSerializer(serializers.Serializer):
    key = serializers.IntegerField(read_only=True)
    is_allowable = serializers.BooleanField()
    accept_monetization = serializers.BooleanField()
    tags = serializers.ListField()

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


class GameCopyrightSerializer(AbstractBaseCopyrightSerializer):
    name = serializers.CharField()
    description = serializers.CharField()

    def create(self, validated_data):
        validated_data.setdefault('key', random_key(8))
        return GameCopyright.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.is_allowable = validated_data.get('is_allowable')
        instance.accept_monetization = validated_data.get('accept_monetization')
        instance.tags = validated_data.get('tags')

        instance.name = validated_data.get('name')
        instance.description = validated_data.get('description')
        instance.save()
        return instance


class SongCopyrightSerializer(AbstractBaseCopyrightSerializer):
    song = serializers.CharField()
    artist = serializers.CharField()
    album = serializers.CharField()
    licensed_to = serializers.CharField()

    def create(self, validated_data):
        validated_data.setdefault('key', random_key(8))
        return SongCopyright.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.is_allowable = validated_data.get('is_allowable')
        instance.accept_monetization = validated_data.get('accept_monetization')
        instance.tags = validated_data.get('tags')

        instance.song = validated_data.get('song')
        instance.artist = validated_data.get('artist')
        instance.album = validated_data.get('album')
        instance.licensed_to = validated_data.get('licensed_to')
        instance.save()
        return instance


class RestrictionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restrictions
        fields = '__all__'
