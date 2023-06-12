"""
This module makes the app package importable and initializes the celery app on import.
"""
# The 'absolute_import' helps avoid confusion between relative and absolute imports,
# and 'unicode_literals' ensures that all string literals in this module are unicode.
from __future__ import absolute_import, unicode_literals

# Import the Celery application instance. The 'app' is the Celery application object.
# We use it to run celery commands.
from .celery import app as celery_app

# The '__all__' variable is a list that defines the public interface of the module.
# It restricts to only allow specific attributes to be accessible when importing
# the module with 'from module import *'. Here, we're only exposing 'celery_app'.
__all__ = ('celery_app',)
