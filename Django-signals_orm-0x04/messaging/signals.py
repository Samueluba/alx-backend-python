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

from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory  # ✅ These must be present

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        try:
            original = Message.objects.get(pk=instance.pk)
            if original.content != instance.content:
                # ✅ Log old content before it's overwritten
                MessageHistory.objects.create(
                    message=original,
                    old_content=original.content,
                    edited_by=instance.sender  # Assuming sender is editor
                )
                instance.edited = True  # ✅ Mark message as edited
        except Message.DoesNotExist:
            pass
