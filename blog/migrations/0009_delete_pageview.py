# Generated by Django 5.0 on 2024-08-28 03:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0008_pageview"),
    ]

    operations = [
        migrations.DeleteModel(
            name="PageView",
        ),
    ]
