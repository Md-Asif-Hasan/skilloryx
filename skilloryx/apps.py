from django.apps import AppConfig


class SkilloryxConfig(AppConfig):
    deafault_auto_field = "django.db.models.BigAutoField"
    name = 'skilloryx'

    def ready(self):
        import skilloryx.signals

