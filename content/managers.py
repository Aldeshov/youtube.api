from django.db import models

from additional.models import Copyrights


class VideoContentManager(models.Manager):
    def create(self, **extra_fields):
        copyrights = Copyrights.objects.create()
        content = self.model(**extra_fields)
        content.copyrights = copyrights
        content.save(using=self._db)
        return content

    def public_contents(self):
        return self.filter(copyrights__is_private=False)

    def adult_contents(self):
        return self.filter(copyrights__is_adult_content=True)

    def kids_contents(self):
        return self.filter(copyrights__is_kids_content=True)


class StatusManager(models.Manager):
    def related(self):
        return self.select_related('owner', 'content')
