from django.apps import AppConfig

class MessagingAppConfig(AppConfig):  # Replace 'MessagingApp' with your app name
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messaging'  # Replace with your app name

    def ready(self):
        import messaging.signals  # Make sure the signals are imported

