from django.core.management.base import BaseCommand
from scraper.tasks import delete_past_shows


class Command(BaseCommand):
    """
    Custom management command to delete past show from database.
    """

    help = 'Delete past show date from database'

    def handle(self, *args, **kwargs):
        """
        Handle the command execution.
        """
        delete_past_shows.delay()
        self.stdout.write(self.style.SUCCESS('Successfully deleted past show date.'))
