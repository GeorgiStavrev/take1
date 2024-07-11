from django.apps import AppConfig
from kafka_writer import create_topic


class BackendAppConfig(AppConfig):
    name = "backend"
    verbose_name = "Backend"

    def ready(self):
        create_topic()
