# Generated by Django 5.1.3 on 2025-02-19 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-created_at'], 'verbose_name': 'Đánh Giá Sản Phẩm', 'verbose_name_plural': 'Danh Sách Đánh Giá Sản Phẩm'},
        ),
    ]
