from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from .models import Product, ProductImage
import os

# Product
# Xóa avatar cũ khi cập nhật ảnh mới
@receiver(pre_save, sender=Product)
def delete_old_avatar_on_update(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_avatar = Product.objects.get(pk=instance.pk).image
        except Product.DoesNotExist:
            return
        new_avatar = instance.image
        if old_avatar and old_avatar != new_avatar and "default.png" not in old_avatar.name:
            if os.path.isfile(old_avatar.path):  # Dùng `.path` thay vì `.name`
                os.remove(old_avatar.path)

# Xóa avatar khi xóa sản phẩm
@receiver(post_delete, sender=Product)
def delete_avatar_on_delete(sender, instance, **kwargs):
    if instance.image and "default.png" not in instance.image.name:
        if os.path.isfile(instance.image.path):  # Dùng `.path`
            os.remove(instance.image.path)
 

# ProductImage
@receiver(pre_save, sender=ProductImage)
def delete_old_image_on_update(sender, instance, **kwargs):
    """Xóa ảnh cũ nếu ảnh mới được tải lên"""
    if instance.pk:  # Nếu sản phẩm đã tồn tại (để tránh trường hợp create mới)
        try:
            old_image = ProductImage.objects.get(pk=instance.pk).image
        except ProductImage.DoesNotExist:
            return
        new_image = instance.image
        if old_image and old_image != new_image:  # Chỉ xóa nếu ảnh thực sự thay đổi
            if os.path.isfile(old_image.path):
                os.remove(old_image.path)

# Xóa ảnh khi xóa ProductImage
@receiver(post_delete, sender=ProductImage)
def delete_image_on_delete(sender, instance, **kwargs):
    """Xóa ảnh khỏi hệ thống khi ProductImage bị xóa"""
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
