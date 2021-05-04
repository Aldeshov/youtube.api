from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models

from applications.managers import ChannelManager
from tools.validators import content_validation, playlist_validation
from youtube.settings import AUTH_USER_MODEL


class Channel(models.Model):
    code = models.CharField(max_length=16,
                            validators=[RegexValidator(regex='^.{16}$', message='Length must be 16', code='mismatch')],
                            unique=True)
    owner = models.OneToOneField(to=AUTH_USER_MODEL, related_name='channel', on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    avatar = models.ImageField(upload_to='channel_avatars/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    description = models.TextField()
    subscribers = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)

    objects = ChannelManager()


# This Validator has been moved here (from tools.validators) due to circular import.
def channel_validation(value):
    if not Channel.objects.is_exists(value):
        raise ValidationError('Channel does not exists')


class Profile(models.Model):
    is_private = models.BooleanField(default=True)
    saved_playlists = ArrayField(
        models.IntegerField(validators=[MinValueValidator(8), MaxValueValidator(8),
                                        playlist_validation], verbose_name="key"),
        null=True,
        blank=True
    )
    saved_contents = ArrayField(
        models.CharField(max_length=16,
                         validators=[RegexValidator(regex='^.{16}$', message='Length has to be 16', code='mismatch'),
                                     content_validation],
                         verbose_name="key"),
        null=True,
        blank=True,
        verbose_name="favorites"
    )
    liked = ArrayField(
        models.CharField(max_length=16,
                         validators=[RegexValidator(regex='^.{16}$', message='Length has to be 16', code='mismatch'),
                                     content_validation],
                         verbose_name="key"),
        null=True,
        blank=True
    )
    disliked = ArrayField(
        models.CharField(max_length=16,
                         validators=[RegexValidator(regex='^.{16}$', message='Length has to be 16', code='mismatch'),
                                     content_validation],
                         verbose_name="key"),
        null=True,
        blank=True
    )
    subscribed = ArrayField(
        models.CharField(max_length=16,
                         validators=[RegexValidator(regex='^.{16}$', message='Length has to be 16', code='mismatch'),
                                     channel_validation],
                         verbose_name="code"),
        null=True,
        blank=True
    )

    @staticmethod
    def is_valid(**arguments):

        if arguments.get('channel'):
            channel_validation(arguments.get('channel'))

        if arguments.get('content'):
            content_validation(arguments.get('channel'))

        if arguments.get('playlist'):
            playlist_validation(arguments.get('channel'))

    def set_private(self, set_public=False):
        self.is_private = True
        if set_public:
            self.is_private = False
        return self

    def save_playlist(self, playlist_key, remove=False):
        """
        The function to save (or remove from saved) playlists

        :param playlist_key: Playlist key to save / remove from saved
        :param remove: To Remove from saved playlists
        :return: Self object
        """

        # Validating Playlist Key
        self.is_valid(playlist=playlist_key)

        for playlist in self.saved_playlists:
            if playlist == playlist_key:
                if remove:
                    self.saved_playlists.remove(playlist)
                    return self
                raise ValueError("Playlist exists")
        if not remove:
            self.saved_playlists.append(playlist_key)
            return self
        raise ValueError("There is no playlist to remove")

    def save_content(self, content_key, remove=False):
        """
        The function to save (or remove from saved) contents

        :param content_key: Content key to save / remove from saved
        :param remove: To Remove from saved contents
        :return: Self object
        """
        # Validating Content Key
        self.is_valid(content=content_key)

        for content in self.saved_contents:
            if content == content_key:
                if remove:
                    self.saved_contents.remove(content)
                    return self
                raise ValueError("Content exists")
        if not remove:
            self.saved_contents.append(content_key)
            return self
        raise ValueError("There is no content to remove")

    def like_content(self, content_key, dislike=False, retract=False):
        """
        The function to add (or remove) liked / disliked videos

        :param content_key: Content Key to Like / Dislike or retract
        :param dislike: To dislike Content
        :param retract: To retract Like / Dislike vote
        :return: Self object
        """
        # Validating Content Key
        self.is_valid(content=content_key)

        if not dislike:
            for like in self.liked:
                if like == content_key:
                    if retract:
                        self.liked.remove(like)
                        return self
                    raise ValueError("Content already liked")
            if retract:
                raise ValueError("There is no LIKE to retract")

        for dislike in self.disliked:
            if dislike == content_key:
                if retract:
                    self.disliked.remove(dislike)
                    return self
                raise ValueError("Content already liked")
        if retract:
            raise ValueError("There is no DISLIKE to retract")

        if dislike:
            self.disliked.append(content_key)
            return self
        self.liked.append(content_key)
        return self

    def subscribe(self, channel_code, unsubscribe=False):
        """
        The function to subscribe (or unsubscribe) to channels

        :param channel_code: Channel key to subscribe / unsubscribe
        :param unsubscribe: To Unsubscribe from channel
        :return: Self object
        """
        # Validating Channel Code
        self.is_valid(channel=channel_code)

        for channel in self.subscribed:
            if channel == channel_code:
                if unsubscribe:
                    self.subscribed.remove(channel)
                    return self
                raise ValueError("Channel already subscribed")
        if not unsubscribe:
            self.subscribed.append(channel_code)
            return self
        raise ValueError("Channel already unsubscribed")
