from django.apps import AppConfig

REDIRECT_PATH = 'http://127.0.0.1:8000/code'

class QrGeneratorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'QR_generator'