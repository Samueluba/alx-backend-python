from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, retrieving, and creating Conversations.
    Also supports adding participants and viewing nested messages.
    """
    queryset = Conversation.objects.all().prefetch_related("participants", "messages")
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        When creating a conversation:
        - Add the current user as a participant automatically.
        - Allow passing a list of participant IDs in request.data["participants"] (optional).
        """
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

        # Optionally add other participants if provided
        participant_ids = self.request.data.get("participants", [])
        if isinstance(participant_ids, list):
            users = User.objects.filter(id__in=participant_ids)
            conversation.participants.add(*users)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating Messages.
    Supports filtering messages by conversation via ?conversation=<id>.
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Message.objects.select_related("sender", "conversation")
        conversation_id = self.request.query_params.get("conversation")
        if conversation_id:
            queryset = queryset.filter(conversation_id=conversation_id)
        return queryset.order_by("timestamp")

    def perform_create(self, serializer):
        """
        When sending a message:
        - Use the authenticated user as the sender.
        - conversation_id must be provided in the POST body.
        """
        conversation_id = self.request.data.get("conversation")
        if not conversation_id:
            raise ValueError("conversation field is required.")
        conversation = Conversation.objects.get(pk=conversation_id)
        serializer.save(sender=self.request.user, conversation=conversation)

