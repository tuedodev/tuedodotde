from django.apps import AppConfig


class WerkstattConfig(AppConfig):
    name = 'werkstatt'

    def ready(self):
            import werkstatt.signals
