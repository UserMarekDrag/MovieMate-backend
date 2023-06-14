from django.apps import AppConfig


class MovieApiConfig(AppConfig):
    """
    Configuration for the Movie Api application.

    This class is used by Django's application registry to configure the movie_api app.
    It contains metadata about the app, like its name and the default type of auto-created primary key field.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movie_api'
