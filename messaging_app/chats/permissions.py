# chats/permissions.py

from rest_framework.permissions import BasePermission

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to allow only participants of a conversation
    to send, view, update, or delete messages.
    """

    def has_permission(self, request, view):
        # ✔️ Check if user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # ✔️ Allow access only if user is in the conversation's participants
        conversation = getattr(obj, 'conversation', None)
        if not conversation:
            return False

        # ✔️ Check method to ensure enforcement on update/delete as well
        if request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
            return request.user in conversation.participants.all()

        return False

