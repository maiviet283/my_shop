from django.db.models.signals import pre_save, post_delete, post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Product, ProductImage, Category
import os


@receiver(pre_save, sender=Product)
def delete_old_product_image(sender, instance, **kwargs):
    """Xóa ảnh cũ khi cập nhật Product.image"""
    if not instance.pk:
        return

    try:
        old_image = Product.objects.get(pk=instance.pk).image
    except Product.DoesNotExist:
        return

    new_image = instance.image
    if old_image and old_image != new_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)


@receiver(post_delete, sender=Product)
def delete_product_image_on_delete(sender, instance, **kwargs):
    """Xóa ảnh khi Product bị xóa"""
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)


# ProductImage
@receiver(pre_save, sender=ProductImage)
def delete_old_productimage_file(sender, instance, **kwargs):
    """Xóa ảnh cũ khi cập nhật ProductImage.image"""
    if not instance.pk:
        return

    try:
        old_image = ProductImage.objects.get(pk=instance.pk).image
    except ProductImage.DoesNotExist:
        return

    new_image = instance.image
    if old_image and old_image != new_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)


@receiver(post_delete, sender=ProductImage)
def delete_productimage_file_on_delete(sender, instance, **kwargs):
    """Xóa ảnh khi ProductImage bị xóa"""
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)


@receiver([post_save, post_delete], sender=Product)
def clear_product_cache(sender, instance, **kwargs):
    cache_key = f"product_{instance.pk}"
    cache.delete(cache_key)

    for page in range(1, 10):  # giả sử tối đa 10 trang
        cache.delete(f"product_list_page_{page}")

@receiver([post_save, post_delete], sender=Category)
def clear_category_cache(sender, instance, **kwargs):
    cache.delete("category_list")