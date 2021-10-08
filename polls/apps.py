"""Configuration of application."""
from django.apps import AppConfig


class PollsConfig(AppConfig):
    """Setting polls config."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
