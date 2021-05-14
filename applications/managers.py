from django.db import models


class ChannelManager(models.Manager):

    def verified_channels(self):
        return self.filter(is_verified=True)

    def get_popular_channels(self, subscribers=100000):
        return [channel for channel in self.all().order_by(subscribers).reverse() if channel.subscribers >= subscribers]
