from rest_framework import serializers

from additional.serializers import CopyrightsSerializer
from applications.models import Profile
from applications.serializers import ChannelSerializer
from content.models import VideoContent, Comment, Status, Playlist


class BaseContentSerializer(serializers.Serializer):
    code = serializers.CharField(read_only=True)
    title = serializers.CharField()
    views = serializers.ReadOnlyField()
    likes = serializers.ReadOnlyField()
    dislikes = serializers.ReadOnlyField()

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


class VideoContentSerializer(BaseContentSerializer):
    video = serializers.FileField()
    type = serializers.IntegerField(min_value=1, max_value=6)
    description = serializers.CharField(min_length=4)
    copyrights = CopyrightsSerializer(read_only=True)

    def create(self, validated_data):
        validated_data.setdefault('on_channel', self.context.get('channel'))
        return VideoContent.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title')
        instance.video = validated_data.get('video')
        instance.type = validated_data.get('type')
        instance.description = validated_data.get('description')
        instance.save()
        return instance


class PlaylistSerializer(serializers.Serializer):
    key = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    contents = VideoContentSerializer(many=True, read_only=True)

    def create(self, validated_data):
        validated_data.setdefault('owner', self.context.get('channel'))
        return Playlist.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title')
        instance.save()
        return instance


class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    owner = ChannelSerializer(read_only=True)
    text = serializers.CharField()

    def create(self, validated_data):
        validated_data.setdefault('owner', self.context.get('channel'))
        validated_data.setdefault('content', self.context.get('content'))
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text')
        instance.save()
        return instance


class StatusSerializer(BaseContentSerializer):
    short_video = serializers.FileField()

    def create(self, validated_data):
        validated_data.setdefault('on_channel', self.context.get('channel'))
        return Status.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title')
        instance.short_videos = validated_data.get('short_video')
        instance.save()
        return instance


class ProfileSerializer(serializers.ModelSerializer):
    """
    Used for only get Information about User profile.
    For Updating Information use functions in Profile() class.
    """
    is_private = serializers.BooleanField(read_only=True)
    saved_playlists = PlaylistSerializer(read_only=True, many=True)
    saved_contents = VideoContentSerializer(read_only=True, many=True)
    subscribed = ChannelSerializer(read_only=True, many=True)

    class Meta:
        model = Profile
        exclude = ('id', )
