from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    List, retrieve and create conversations.
    Supports search by conversation name or participant username.
    """
    queryset = Conversation.objects.all().prefetch_related("participants", "messages")
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "participants__username"]

    def perform_create(self, serializer):
        conversation = serializer.save()
        # add creator automatically
        conversation.participants.add(self.request.user)

        # optionally add more participants
        participant_ids = self.request.data.get("participants", [])
        if isinstance(participant_ids, list):
            users = User.objects.filter(id__in=participant_ids)
            conversation.participants.add(*users)


class MessageViewSet(viewsets.ModelViewSet):
    """
    List and send messages.
    Filter by conversation using ?conversation=<id>.
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["timestamp"]
    ordering = ["timestamp"]

    def get_queryset(self):
        queryset = Message.objects.select_related("sender", "conversation")
        conversation_id = self.request.query_params.get("conversation")
        if conversation_id:
            queryset = queryset.filter(conversation_id=conversation_id)
        return queryset

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get("conversation")
        content = request.data.get("content")

        if not conversation_id or not content:
            return Response(
                {"detail": "Both 'conversation' and 'content' are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            conversation = Conversation.objects.get(pk=conversation_id)
        except Conversation.DoesNotExist:
            return Response(
                {"detail": "Conversation not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(
            data={"conversation": conversation.id, "content": content}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=request.user, conversation=conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# chats/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Message
from .serializers import MessageSerializer
from .permissions import IsParticipantOfConversation

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]  # ✔️ Custom + auth

    def get_queryset(self):
        # ✔️ Restrict messages to conversations the user participates in
        return Message.objects.filter(conversation__participants=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        message = self.get_object()

        # ✔️ Explicit permission check and HTTP_403_FORBIDDEN
        if request.user not in message.conversation.participants.all():
            return Response(
                {"detail": "You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(message)
        return Response(serializer.data)

