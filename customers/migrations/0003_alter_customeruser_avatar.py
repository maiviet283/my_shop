# Generated by Django 5.1.3 on 2025-02-17 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_alter_customeruser_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customeruser',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='customers/avatars/%Y/%m/'),
        ),
    ]
