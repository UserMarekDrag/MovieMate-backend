# Generated by Django 4.2 on 2023-06-04 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_api', '0002_rename_movie_searchhistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchhistory',
            name='showing_date',
            field=models.DateField(),
        ),
    ]
