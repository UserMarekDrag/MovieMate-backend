# Generated by Django 4.2 on 2023-08-30 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0004_cinema_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='cinema',
            name='number',
            field=models.IntegerField(null=True),
        ),
    ]
