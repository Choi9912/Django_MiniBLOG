# Generated by Django 5.0 on 2024-08-24 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='author_username',
        ),
        migrations.AddField(
            model_name='comment',
            name='level',
            field=models.IntegerField(default=0),
        ),
    ]