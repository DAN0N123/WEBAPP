# Generated by Django 5.0 on 2024-01-08 17:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_customuser_date_joined'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='favorites',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='date_joined',
            field=models.TimeField(default=datetime.datetime(2024, 1, 8, 17, 20, 11, 327222, tzinfo=datetime.timezone.utc)),
        ),
    ]
