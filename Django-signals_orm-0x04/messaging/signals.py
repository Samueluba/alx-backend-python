from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification

@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    """
    This signal is triggered when a new Message is saved.
    It automatically creates a Notification for the receiver.
    """
    if created:  # Ensure it's only triggered on message creation
        Notification.objects.create(
            user=instance.receiver,  # The user receiving the message
            message=instance,        # The actual message
        )

