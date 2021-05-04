from django.core.exceptions import ValidationError

from content.models import Content, Playlist


def content_validation(value):
    if not Content.objects.is_exists(value):
        raise ValidationError('Content does not exists')


def playlist_validation(value):
    if not Playlist.objects.is_exists(value):
        raise ValidationError('Playlist does not exist')
