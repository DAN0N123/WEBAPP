# Generated by Django 5.0 on 2024-01-08 18:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_customuser_favorites_alter_customuser_cart_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_sent', models.TimeField(default=datetime.datetime(2024, 1, 8, 18, 30, 59, 384236, tzinfo=datetime.timezone.utc))),
                ('message', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='customuser',
            name='date_joined',
            field=models.TimeField(default=datetime.datetime(2024, 1, 8, 18, 30, 59, 385236, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AddField(
            model_name='customuser',
            name='messages',
            field=models.ManyToManyField(blank=True, related_name='messages', to='store.message'),
        ),
    ]
