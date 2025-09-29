from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class MessagingTestCase(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='alice', password='password123')
        self.receiver = User.objects.create_user(username='bob', password='password123')

    def test_message_creation_creates_notification(self):
        # Ensure no notifications exist at start
        self.assertEqual(Notification.objects.count(), 0)

        # Create a new message
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content='Hello Bob!'
        )

        # There should be one notification for the receiver
        notifications = Notification.objects.filter(user=self.receiver)
        self.assertEqual(notifications.count(), 1)

        notification = notifications.first()
        self.assertEqual(notification.message, message)
        self.assertFalse(notification.is_read)

