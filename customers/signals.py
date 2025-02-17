from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from .models import CustomerUser
from django.conf import settings
import os


# Xóa avatar cũ khi cập nhật ảnh mới
@receiver(pre_save, sender=CustomerUser)
def delete_old_avatar_on_update(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_avatar = CustomerUser.objects.get(pk=instance.pk).avatar
        except CustomerUser.DoesNotExist:
            return
        new_avatar = instance.avatar
        if old_avatar and old_avatar != new_avatar and "default.png" not in old_avatar.name:
            old_avatar_path = os.path.join(settings.MEDIA_ROOT, old_avatar.name)
            if os.path.exists(old_avatar_path):
                os.remove(old_avatar_path)

# Xóa avatar khi xóa tài khoản
@receiver(post_delete, sender=CustomerUser)
def delete_avatar_on_delete(sender, instance, **kwargs):
    if instance.avatar and "default.png" not in instance.avatar.name:
        avatar_path = os.path.join(settings.MEDIA_ROOT, instance.avatar.name)
        if os.path.exists(avatar_path):
            os.remove(avatar_path)
