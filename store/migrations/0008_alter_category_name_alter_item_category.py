# Generated by Django 5.0 on 2024-01-06 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_alter_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('Other', 'Other'), ('Decoration', 'Decoration'), ('Food', 'Food'), ('One_Piece', 'One_Piece'), ('Electronics', 'Electronics')], max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.ManyToManyField(blank=True, null=True, to='store.category'),
        ),
    ]