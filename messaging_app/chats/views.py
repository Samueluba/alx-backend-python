from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, retrieving, and creating Conversations.
    Includes search & filter capabilities.
    """
    queryset = Conversation.objects.all().prefetch_related("participants", "messages")
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "participants__username"]  # search by conversation name or participant username

    def perform_create(self, serializer):
        """
        Create a new conversation and automatically add
        the current user as a participant.
        """
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

        # Optionally add other participants
        participant_ids = self.request.data.get("participants", [])
        if isinstance(participant_ids, list):
            users = User.objects.filter(id__in=participant_ids)
            conversation.participants.add(*users)

    @action(detail=True, methods=["get"])
    def participants(self, request, pk=None):
        """Custom endpoint to list participants of a conversation."""
        conversation = self.get_object()
        users = conversation.participants.all()
        return Response(
            {"participants": [u.username for u in users]},
            status=status.HTTP_200_OK
        )


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating Messages.
    Supports filtering messages

    from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet

# ✅ Create a DRF DefaultRouter instance
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    # ✅ Include all automatically generated routes
    path('', include(router.urls)),
]

