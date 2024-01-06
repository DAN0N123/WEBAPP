# Generated by Django 5.0 on 2024-01-06 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_alter_category_name_alter_item_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('Other', 'Other'), ('Decoration', 'Decoration'), ('Food', 'Food'), ('OnePiece', 'OnePiece'), ('Electronics', 'Electronics')], max_length=40, unique=True),
        ),
    ]