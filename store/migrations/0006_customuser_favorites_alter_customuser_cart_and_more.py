# Generated by Django 5.0 on 2024-01-08 17:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_item_favorites_alter_customuser_date_joined'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='favorites',
            field=models.ManyToManyField(blank=True, related_name='favorite_items', to='store.item'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='cart',
            field=models.ManyToManyField(blank=True, related_name='cart_items', to='store.item'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='date_joined',
            field=models.TimeField(default=datetime.datetime(2024, 1, 8, 17, 44, 38, 902796, tzinfo=datetime.timezone.utc)),
        ),
    ]
