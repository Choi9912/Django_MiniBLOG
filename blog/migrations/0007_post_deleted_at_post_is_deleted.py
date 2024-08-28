# Generated by Django 5.0 on 2024-08-27 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0006_remove_category_created_at_remove_category_is_public_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="deleted_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="post",
            name="is_deleted",
            field=models.BooleanField(default=False),
        ),
    ]