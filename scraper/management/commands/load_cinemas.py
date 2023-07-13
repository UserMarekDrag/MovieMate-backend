import json
from django.core.management.base import BaseCommand
from scraper.models import Cinema


class Command(BaseCommand):
    """
    Custom management command to load cinema data from cinemas.json.
    """

    help = 'Loads cinema data from cinemas.json'

    def handle(self, *args, **kwargs):
        """
        Handle the command execution.
        """
        with open('cities.json', 'r', encoding='utf-8') as file:
            cinemas = json.load(file)

        for cinema in cinemas:
            Cinema.objects.update_or_create(
                name=cinema['name'],
                city=cinema['city'],
                defaults={'address': cinema['address']},
            )

        self.stdout.write(self.style.SUCCESS('Successfully updated cinema data.'))
