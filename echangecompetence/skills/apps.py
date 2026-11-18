from django.apps import AppConfig
from utils.log import LogError


class SkillsConfig(AppConfig, LogError):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'skills'
