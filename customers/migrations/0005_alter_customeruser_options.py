# Generated by Django 5.1.3 on 2025-02-23 16:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0004_alter_customeruser_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customeruser',
            options={'verbose_name': 'Khách Hàng', 'verbose_name_plural': 'Khách Hàng'},
        ),
    ]
