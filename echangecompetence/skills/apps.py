from django.apps import AppConfig
from .user import create_user


class SkillsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'skills'
    create_user()
