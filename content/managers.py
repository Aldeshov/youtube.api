from django.db import models


class BaseContentManager(models.Manager):

    def is_exists(self, content_key):
        return self.filter(key__exact=content_key).exists()


class PlaylistManager(models.Manager):

    def is_exists(self, content_key):
        return self.filter(key__exact=content_key).exists()
