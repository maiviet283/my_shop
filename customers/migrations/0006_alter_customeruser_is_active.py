# Generated by Django 5.1.6 on 2025-03-11 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0005_alter_customeruser_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customeruser',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
