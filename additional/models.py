from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class AbstractBaseCopyright(models.Model):
    key = models.IntegerField(validators=[MinValueValidator(8), MaxValueValidator(8)], unique=True)
    is_allowable = models.BooleanField(default=True)
    accept_monetization = models.BooleanField(default=True)
    tags = ArrayField(
        models.CharField(max_length=64),
        null=True,
        blank=True
    )


class GameCopyright(AbstractBaseCopyright):
    name = models.CharField(max_length=64)
    description = models.TextField()


class SongCopyright(AbstractBaseCopyright):
    song = models.CharField(max_length=64)
    artist = models.CharField(max_length=64)
    album = models.CharField(max_length=64)
    licensed_to = models.TextField()


class Restrictions(models.Model):
    is_private = models.BooleanField(default=False)
    is_adult_content = models.BooleanField(default=False)
    is_kids_content = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Content Restrictions'
        verbose_name_plural = 'Contents Restrictions'
