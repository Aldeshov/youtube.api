from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver

from applications.models import Channel
from tools.upload import file_delete


@receiver(post_delete, sender=Channel)
def channel_deleted(sender, instance, **kwargs):
    if instance.avatar:
        file_delete(instance.avatar)


@receiver(pre_save, sender=Channel)
def channel_changed(sender, instance, **kwargs):
    old_avatar = sender.objects.get(id=instance.id).avatar
    if old_avatar and old_avatar != instance.avatar:
        file_delete(old_avatar)
