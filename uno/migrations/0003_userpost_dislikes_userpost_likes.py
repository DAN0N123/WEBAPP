# Generated by Django 5.0 on 2023-12-29 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uno', '0002_userpost_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpost',
            name='dislikes',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userpost',
            name='likes',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
