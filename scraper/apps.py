from django.apps import AppConfig


class ScraperConfig(AppConfig):
    """
    Configuration for the Scraper application.

    This class is used by Django's application registry to configure the scraper app.
    It contains metadata about the app, like its name and the default type of auto-created primary key field.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scraper'
