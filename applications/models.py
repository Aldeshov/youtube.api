from django.db import models

from applications.managers import ChannelManager
from content.models import Playlist, VideoContent
from tools.random_generate import random_code
from youtube.settings import AUTH_USER_MODEL


class Channel(models.Model):
    code = models.CharField(max_length=16, default=random_code, unique=True)
    owner = models.OneToOneField(to=AUTH_USER_MODEL, related_name='channel', on_delete=models.RESTRICT)
    name = models.CharField(max_length=32)
    avatar = models.ImageField(upload_to='avatars/channel/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    objects = ChannelManager()

    @property
    def subscribers(self):
        return len(self.channel_subscribers.all())

    def __str__(self):
        return f'#{self.code} ({self.name})'


class Profile(models.Model):
    is_private = models.BooleanField(default=True)
    saved_playlists = models.ManyToManyField(Playlist, blank=True)
    saved_contents = models.ManyToManyField(VideoContent, blank=True)
    subscribed = models.ManyToManyField(Channel, related_name='channel_subscribers', blank=True)

    def save_content(self, content, undo=False):
        if undo:
            self.saved_contents.remove(content)
            return

        self.saved_contents.add(content)
        return

    def save_playlist(self, playlist, undo=False):
        if undo:
            self.saved_playlists.remove(playlist)
            return

        self.saved_playlists.add(playlist)
        return

    def subscribe(self, channel, undo=False):
        if undo:
            self.subscribed.remove(channel)
            return

        self.subscribed.add(channel)
        return

    def is_subscribed(self, channel):
        return channel in self.subscribed.all()
