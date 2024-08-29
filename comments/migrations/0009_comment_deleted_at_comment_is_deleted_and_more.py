# Generated by Django 5.0 on 2024-08-29 00:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "comments",
            "0008_remove_comment_deleted_at_remove_comment_is_deleted_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="deleted_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="comment",
            name="is_deleted",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="comment",
            name="parent_comment",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="replies",
                to="comments.comment",
            ),
        ),
        migrations.DeleteModel(
            name="Reply",
        ),
    ]
