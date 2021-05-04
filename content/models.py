from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models

from additional.models import Restrictions
from applications.types import TYPES
from content.managers import BaseContentManager, PlaylistManager
from youtube.settings import CHANNEL_MODEL


class AbstractBaseContent(models.Model):
    key = models.CharField(max_length=16,
                           validators=[RegexValidator(regex='^.{16}$', message='Length has to be 16', code='mismatch')],
                           unique=True)
    title = models.CharField(max_length=64)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    objects = BaseContentManager()

    def report(self):
        pass

    def view_content(self, user):
        if user.is_authenticated:
            self.views += 1
        return self

    def like_content(self, user, dislike=False, retract=False):
        if user.is_authenticated:
            user.profile.like_content(self.key, dislike, retract)
            if not dislike:
                if retract:
                    self.likes -= 1
                else:
                    self.likes += 1
                return self

            if retract:
                self.dislikes -= 1
            else:
                self.dislikes += 1
            return self
        raise ValueError("User not authenticated")

    @property
    def likes_percentage(self):
        total = self.likes + self.dislikes
        if total == 0:
            return -1
        return round((self.likes / total) * 100, 2)

    @staticmethod
    def compare_contents(first, second):
        if first.views == 0 or second.views == 0:
            return -1

        first_content = round(first.likes / (first.likes + first.dislikes)) * first.views
        second_content = round(second.likes / (second.likes + second.dislikes)) * second.views

        return first_content > second_content

    def __str__(self):
        return f'#{self.key} ({self.title})'


class Comment(models.Model):
    owner = models.ForeignKey(to=CHANNEL_MODEL, related_name="comments", on_delete=models.DO_NOTHING)
    text = models.CharField(max_length=255)
    on_content = models.ForeignKey(AbstractBaseContent, related_name="comments", on_delete=models.CASCADE)


class Playlist(models.Model):
    key = models.IntegerField(validators=[MinValueValidator(8), MaxValueValidator(8)], unique=True)
    title = models.CharField(max_length=64)
    owner = models.ForeignKey(to=CHANNEL_MODEL, related_name="playlists", on_delete=models.CASCADE)

    objects = PlaylistManager()


class Content(AbstractBaseContent):
    video = models.FileField()
    type = models.PositiveSmallIntegerField(choices=TYPES, blank=True)
    description = models.TextField()
    on_channel = models.ForeignKey(to=CHANNEL_MODEL, related_name="contents", on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, on_delete=models.DO_NOTHING, related_name="contents", null=True, blank=True)
    copyrights = ArrayField(
        models.IntegerField(validators=[MinValueValidator(8), MaxValueValidator(8)]),
        blank=True
    )
    restrictions = models.OneToOneField(Restrictions, on_delete=models.CASCADE)


class Status(AbstractBaseContent):
    short_videos = ArrayField(
        models.FileField(),
        max_length=5
    )
    on_channel = models.OneToOneField(to=CHANNEL_MODEL, related_name="status", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Statuses'


class CommunityContent(AbstractBaseContent):
    text = models.TextField()
    on_channel = models.ForeignKey(to=CHANNEL_MODEL, related_name="community_contents", on_delete=models.CASCADE)
