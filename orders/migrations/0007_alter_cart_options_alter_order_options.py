# Generated by Django 5.1.3 on 2025-02-23 16:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_remove_order_items_orderitem'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'verbose_name': 'Giỏ Hàng', 'verbose_name_plural': 'Giỏ Hàng'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Đơn Hàng', 'verbose_name_plural': 'Đơn Hàng'},
        ),
    ]
