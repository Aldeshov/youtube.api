from rest_framework import serializers

from additional.models import GameCopyright, SongCopyright, Copyrights


class BaseCopyrightSerializer(serializers.Serializer):
    key = serializers.IntegerField(read_only=True)
    is_allowable = serializers.BooleanField()
    accept_monetization = serializers.BooleanField()
    tags = serializers.ListField()

    def validate_accept_monetization(self, value):
        if value and not self.is_allowable:
            raise serializers.ValidationError('Copyright not allowable for monetization')
        return value

    def validate_is_allowable(self, value):
        if value is False and self.accept_monetization:
            raise serializers.ValidationError('Copyright first need to decline monetization')
        return value

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


class GameCopyrightSerializer(BaseCopyrightSerializer):
    name = serializers.CharField()
    description = serializers.CharField()

    def create(self, validated_data):
        return GameCopyright.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.is_allowable = validated_data.get('is_allowable')
        instance.accept_monetization = validated_data.get('accept_monetization')
        instance.tags = validated_data.get('tags')

        instance.name = validated_data.get('name')
        instance.description = validated_data.get('description')
        instance.save()
        return instance


class SongCopyrightSerializer(BaseCopyrightSerializer):
    song = serializers.CharField()
    artist = serializers.CharField()
    album = serializers.CharField()
    licensed_to = serializers.CharField()

    def create(self, validated_data):
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


class CopyrightsSerializer(serializers.ModelSerializer):
    is_adult_content = serializers.BooleanField()
    is_kids_content = serializers.BooleanField()

    song_copyrights = SongCopyrightSerializer(read_only=True, many=True)
    game_copyrights = GameCopyrightSerializer(read_only=True, many=True)

    class Meta:
        model = Copyrights
        fields = '__all__'

    def validate_is_adult_content(self, value):
        if value and self.is_kids_content:
            raise serializers.ValidationError('Cannot be True both kids & adults content')
        return value

    def validate_is_kids_content(self, value):
        if value and self.is_adult_content:
            raise serializers.ValidationError('Cannot be True both kids & adults content')
        return value
