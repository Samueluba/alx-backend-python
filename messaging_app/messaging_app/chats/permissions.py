# messaging_app/chats/permissions.py

from rest_framework import permissions

class IsParticipant(permissions.BasePermission):
    """
    Permission to allow only participants of a conversation or message to access it.
    Assumes the view has `.get_object()` or `.queryset` methods and object has attributes like `.participants` or `.sender/receiver`.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Example for a Conversation model with participants ManyToMany
        if hasattr(obj, 'participants'):
            return user in obj.participants.all()

        # Example for a Message model with sender or receiver
        if hasattr(obj, 'sender') and hasattr(obj, 'receiver'):
            return (obj.sender == user) or (obj.receiver == user)

        # Fallback: deny
        return False

