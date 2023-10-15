from django.apps import AppConfig


class MailerConfig(AppConfig):
    """
    Configuration for the Mailer application.

    This class is used by Django's application registry to configure the mailer app.
    It contains metadata about the app, like its name and the default type of auto-created primary key field.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailer'
