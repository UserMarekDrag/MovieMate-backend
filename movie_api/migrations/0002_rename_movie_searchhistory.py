# Generated by Django 4.2 on 2023-06-04 14:52

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movie_api', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Movie',
            new_name='SearchHistory',
        ),
    ]
