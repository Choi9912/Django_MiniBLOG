# Generated by Django 5.0 on 2024-08-23 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_remove_notification_user_delete_bookmark_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='is_removed',
            field=models.BooleanField(default=False),
        ),
    ]