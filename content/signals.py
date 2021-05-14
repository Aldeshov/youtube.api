from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from content.models import VideoContent, Status
from tools.upload import file_delete


@receiver(post_delete, sender=VideoContent)
def content_deleted(sender, instance, **kwargs):
    instance.copyrights.delete()

    if instance.video:
        file_delete(instance.video)


@receiver(pre_save, sender=VideoContent)
def content_changed(sender, instance, **kwargs):
    old_video = sender.objects.get(id=instance.id).video
    if old_video and old_video != instance.video:
        file_delete(old_video)


@receiver(post_delete, sender=Status)
def status_deleted(sender, instance, **kwargs):
    if instance.short_video:
        file_delete(instance.short_video)


@receiver(pre_save, sender=Status)
def status_changed(sender, instance, **kwargs):
    old_video = sender.objects.get(id=instance.id).short_video
    if old_video and old_video != instance.short_video:
        file_delete(old_video)
