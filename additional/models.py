from django.contrib.postgres.fields import ArrayField
from django.db import models

from tools.random_generate import random_key


class BaseCopyright(models.Model):
    key = models.IntegerField(default=random_key, primary_key=True)
    is_allowable = models.BooleanField(default=True)
    accept_monetization = models.BooleanField(default=True)
    tags = ArrayField(
        models.CharField(max_length=64),
        null=True,
        blank=True
    )

    class Meta:
        abstract = True


class GameCopyright(BaseCopyright):
    name = models.CharField(max_length=64)
    description = models.TextField()


class SongCopyright(BaseCopyright):
    song = models.CharField(max_length=64)
    artist = models.CharField(max_length=64)
    album = models.CharField(max_length=64)
    licensed_to = models.TextField()


class Copyrights(models.Model):
    is_private = models.BooleanField(default=False)
    is_adult_content = models.BooleanField(default=False)
    is_kids_content = models.BooleanField(default=False)

    song_copyrights = models.ManyToManyField(SongCopyright, blank=True)
    game_copyrights = models.ManyToManyField(GameCopyright, blank=True)

    class Meta:
        verbose_name = "Content's copyrights"
        verbose_name_plural = "All Contents' copyrights"
