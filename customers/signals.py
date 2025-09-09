from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from .models import CustomerUser
import os


@receiver(pre_save, sender=CustomerUser)
def delete_old_avatar_on_update(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_avatar = CustomerUser.objects.get(pk=instance.pk).avatar
    except CustomerUser.DoesNotExist:
        return

    new_avatar = instance.avatar
    if old_avatar and old_avatar != new_avatar:
        old_path = os.path.join(settings.MEDIA_ROOT, old_avatar.name)
        if os.path.isfile(old_path):
            os.remove(old_path)


@receiver(post_delete, sender=CustomerUser)
def delete_avatar_on_delete(sender, instance, **kwargs):
    if instance.avatar:
        path = os.path.join(settings.MEDIA_ROOT, instance.avatar.name)
        if os.path.isfile(path):
            os.remove(path)
