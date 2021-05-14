from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from authentication.models import User
from tools.upload import file_delete


@receiver(post_delete, sender=User)
def user_deleted(sender, instance, **kwargs):
    instance.profile.delete()

    if instance.avatar:
        file_delete(instance.avatar)


@receiver(pre_save, sender=User)
def user_changed(sender, instance, **kwargs):
    old_avatar = sender.objects.get(id=instance.id).avatar
    if old_avatar and old_avatar != instance.avatar:
        file_delete(old_avatar)
