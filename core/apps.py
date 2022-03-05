from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        # Implicitly connect a signal handlers decorated with @receiver.
        import core.signals
