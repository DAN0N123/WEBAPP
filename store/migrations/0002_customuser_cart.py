# Generated by Django 5.0 on 2024-01-07 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='cart',
            field=models.ManyToManyField(blank=True, to='store.item'),
        ),
    ]
