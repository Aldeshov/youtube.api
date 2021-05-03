from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models

from applications.managers import ChannelManager
from youtube.settings import AUTH_USER_MODEL


class Profile(models.Model):
    is_private = models.BooleanField(default=True)
    saved_playlists = ArrayField(
        models.IntegerField(validators=[MinValueValidator(8), MaxValueValidator(8)], verbose_name="key"),
        null=True,
        blank=True
    )
    saved_contents = ArrayField(
        models.CharField(max_length=16,
                         validators=[RegexValidator(regex='^.{16}$', message='Length has to be 16', code='mismatch')],
                         verbose_name="key"),
        null=True,
        blank=True,
        verbose_name="favorites"
    )
    liked = ArrayField(
        models.CharField(max_length=16,
                         validators=[RegexValidator(regex='^.{16}$', message='Length has to be 16', code='mismatch')],
                         verbose_name="key"),
        null=True,
        blank=True
    )
    disliked = ArrayField(
        models.CharField(max_length=16,
                         validators=[RegexValidator(regex='^.{16}$', message='Length has to be 16', code='mismatch')],
                         verbose_name="key"),
        null=True,
        blank=True
    )
    subscribed = ArrayField(
        models.CharField(max_length=16,
                         validators=[RegexValidator(regex='^.{16}$', message='Length has to be 16', code='mismatch')],
                         verbose_name="code"),
        null=True,
        blank=True
    )

    def set_private(self, set_public=False):
        if set_public:
            self.is_private = False
            self.save()
            return 0
        self.is_private = True
        self.save()
        return 1

    def save_playlist(self, playlist_key, remove=False):
        """
        The function to save (or remove from saved) playlists

        :param playlist_key: Playlist key to save / remove from saved
        :param remove: To Remove from saved playlists
        :return: Return Key (Done : True, Not Done : False)
        """
        for playlist in self.saved_playlists:
            if playlist == playlist_key:
                if remove:
                    self.saved_playlists.remove(playlist)
                    self.save()
                    return True
                return False
            self.saved_playlists.add(playlist_key)
            self.save()
            return True

    def save_content(self, content_key, remove=False):
        """
        The function to save (or remove from saved) contents

        :param content_key: Content key to save / remove from saved
        :param remove: To Remove from saved contents
        :return: Return Key (Done : True, Not Done : False)
        """
        for content in self.saved_contents:
            if content == content_key:
                if remove:
                    self.saved_contents.remove(content)
                    self.save()
                    return True
                return False
            self.saved_contents.add(content_key)
            self.save()
            return True

    def like_content(self, content_key, dislike=False, retract=False):
        """
        The function to add (or remove) liked / disliked videos

        :param content_key: Content Key to Like / Dislike or retract
        :param dislike: To dislike Content
        :param retract: To retract Like / Dislike vote
        :return: Vote Key (like, dislike, none)
        """

        class ReturnKey:
            """
            Return Key for Content Like / Dislike
            """
            NONE = 0
            LIKE = 1
            DISLIKE = 2

        for like in self.liked:
            if like == content_key:
                if retract:
                    self.liked.remove(like)
                    self.save()
                    return ReturnKey.LIKE
                return ReturnKey.NONE

        for dislike in self.disliked:
            if dislike == content_key:
                if retract:
                    self.disliked.remove(dislike)
                    self.save()
                    return ReturnKey.DISLIKE
                return ReturnKey.NONE

        if dislike:
            self.disliked.add(content_key)
            self.save()
            return ReturnKey.DISLIKE
        self.liked.add(content_key)
        self.save()
        return ReturnKey.LIKE

    def subscribe(self, channel_key, unsubscribe=False):
        """
        The function to subscribe (or unsubscribe) to channels

        :param channel_key: Channel key to subscribe / unsubscribe
        :param unsubscribe: To Unsubscribe from channel
        :return: Return Key (Done : True, Not Done : False)
        """
        for channel in self.subscribed:
            if channel == channel_key:
                if unsubscribe:
                    self.subscribed.remove(channel)
                    self.save()
                    return True
                return False
            self.subscribed.add(channel_key)
            self.save()
            return True


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
