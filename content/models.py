from django.db import models

from additional.models import Copyrights
from applications.types import TYPES
from content.managers import VideoContentManager
from tools.random_generate import random_code, random_key
from tools.validators import validate_size, validate_extension
from youtube.settings import CHANNEL_MODEL


class BaseContent(models.Model):
    code = models.CharField(max_length=16, default=random_code, unique=True)
    title = models.CharField(max_length=64)
    created_on = models.DateTimeField(auto_now_add=True)
    _viewed = models.ManyToManyField(to=CHANNEL_MODEL, related_name='%(app_label)s_%(class)s_views', blank=True)
    _liked = models.ManyToManyField(to=CHANNEL_MODEL, related_name='%(app_label)s_%(class)s_likes', blank=True)
    _disliked = models.ManyToManyField(to=CHANNEL_MODEL, related_name='%(app_label)s_%(class)s_dislikes', blank=True)

    class Meta:
        abstract = True

    def view_content(self, channel):
        self._viewed.add(channel)
        return

    def like_content(self, channel, dislike=False, retract=False):
        if retract:
            self._liked.remove(channel)
            self._disliked.remove(channel)
            return

        if dislike:
            self._liked.remove(channel)
            self._disliked.add(channel)
            return

        self._disliked.remove(channel)
        self._liked.add(channel)
        return

    @property
    def views(self):
        return len(self._viewed.all())

    @property
    def likes(self):
        return len(self._liked.all())

    @property
    def dislikes(self):
        return len(self._disliked.all())

    @property
    def likes_percentage(self):
        if self.dislikes == 0:
            return 1
        return round(self.likes / (self.likes + self.dislikes), 2)

    @staticmethod
    def compare_contents(first, second):
        if first.views == 0 or second.views == 0:
            return -1

        first_content = round(first.likes / (first.likes + first.dislikes)) * first.views
        second_content = round(second.likes / (second.likes + second.dislikes)) * second.views

        return first_content > second_content

    def __str__(self):
        return f'#{self.code} ({self.title})'


class VideoContent(BaseContent):
    video = models.FileField(upload_to='contents', validators=[validate_size, validate_extension])
    preview = models.ImageField(upload_to='previews/')
    type = models.PositiveSmallIntegerField(choices=TYPES, blank=True)
    description = models.TextField()
    on_channel = models.ForeignKey(to=CHANNEL_MODEL, related_name="contents", on_delete=models.CASCADE)
    copyrights = models.OneToOneField(Copyrights, on_delete=models.RESTRICT)

    objects = VideoContentManager()


class Playlist(models.Model):
    key = models.IntegerField(default=random_key, unique=True)
    title = models.CharField(max_length=64)
    owner = models.ForeignKey(to=CHANNEL_MODEL, related_name="playlists", on_delete=models.CASCADE)
    contents = models.ManyToManyField(VideoContent, blank=True)

    def __str__(self):
        return f'#{self.key} ({self.title})'


class Comment(models.Model):
    owner = models.ForeignKey(to=CHANNEL_MODEL, related_name="comments", on_delete=models.DO_NOTHING)
    text = models.CharField(max_length=255)
    content = models.ForeignKey(VideoContent, related_name='comments', on_delete=models.CASCADE)


class Status(BaseContent):
    short_video = models.FileField(upload_to='statuses', validators=[validate_size, validate_extension])
    on_channel = models.OneToOneField(to=CHANNEL_MODEL, related_name="status", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Statuses'
