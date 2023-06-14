from django.apps import AppConfig


class UserApiConfig(AppConfig):
    """
    Configuration for the User Api application.

    This class is used by Django's application registry to configure the user_api app.
    It contains metadata about the app, like its name and the default type of auto-created primary key field.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_api'
