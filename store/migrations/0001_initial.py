# Generated by Django 5.0 on 2024-01-04 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='item_images/')),
                ('price', models.CharField(default='', max_length=30)),
                ('category', models.CharField(default='General', max_length=40)),
                ('name', models.CharField(max_length=40)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
    ]