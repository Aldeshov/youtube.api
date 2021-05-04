from django.db import models


class ChannelManager(models.Manager):

    def verified_channels(self):
        return self.filter(is_verified=True)

    def get_popular_channels(self, subscribers=100000):
        return [channel for channel in self.all().order_by(subscribers).reverse() if channel.subscribers >= subscribers]

    def subscribed_channels(self, user):
        return self.filter(code__in=user.subscribed)

    def is_exists(self, channel_code):
        return self.filter(code__exact=channel_code).exists()
