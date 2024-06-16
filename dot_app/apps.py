"""Basic django file."""
from django.apps import AppConfig


class DotAppConfig(AppConfig):
    """Configuration class for dot application.

    Args:
        AppConfig (_type_): django base inheritance
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dot_app'
