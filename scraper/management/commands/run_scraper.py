import json
from django.core.management.base import BaseCommand
from scraper.tasks import scrape_and_store_multikino, scrape_and_store_helios


with open('cities.json', 'r', encoding='utf-8') as file:
    CITIES = json.load(file)


class Command(BaseCommand):
    """
    Custom management command to run the scraper tasks.
    """

    help = 'Runs the scraper tasks'

    def add_arguments(self, parser):
        """
        Add command line arguments.
        """
        parser.add_argument(
            '-a', '--all',
            action='store_true',
            help='Run tasks for all cinemas'
        )
        parser.add_argument(
            '-c', '--cinema',
            type=str,
            help='Run task for a specific cinema'
        )

    def handle(self, *args, **kwargs):
        """
        Handle the command execution.
        """
        all_cinemas = kwargs['all']
        specific_cinema = kwargs['cinema']

        cities_multikino = CITIES['multikino']  # List of cities for Multikino
        cities_helios = CITIES['helios']  # Dict of cities and cinema numbers for Helios

        if all_cinemas:
            scrape_and_store_multikino.delay(cities_multikino)
            scrape_and_store_helios.delay(cities_helios)
            self.stdout.write(self.style.SUCCESS('Successfully run tasks for all cinemas'))
        elif specific_cinema:
            if specific_cinema.lower() == 'multikino':
                scrape_and_store_multikino.delay(cities_multikino)
                self.stdout.write(self.style.SUCCESS('Successfully run task for Multikino'))
            elif specific_cinema.lower() == 'helios':
                scrape_and_store_helios.delay(cities_helios)
                self.stdout.write(self.style.SUCCESS('Successfully run task for Helios'))
        else:
            self.stdout.write(self.style.ERROR('Please specify the cinema or use -a for all cinemas'))
