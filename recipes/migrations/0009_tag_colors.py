# Generated by Django 3.1.4 on 2021-01-01 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_auto_20201226_1020'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='colors',
            field=models.SlugField(default='Black', verbose_name='Цвет тега'),
        ),
    ]