from rest_framework import permissions
from rest_framework.permissions import BasePermission


from rest_framework import permissions
from rest_framework.permissions import BasePermission

class IsParticipant(BasePermission):
    """
    Custom permission that allows only participants (sender/receiver or conversation members)
    to access the object.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user

        # If the object has a 'participants' attribute (e.g., Conversation)
        if hasattr(obj, 'participants'):
            return user in obj.participants.all()

        # If it's a Message with sender/receiver
        if hasattr(obj, 'sender') and hasattr(obj, 'receiver'):
            return obj.sender == user or obj.receiver == user

        return False
from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access messages.
    """

    def has_permission(self, request, view):
        # Ensure user is authenticated for all views
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is a participant of the conversation.
        'obj' is a Message instance. It should have a 'conversation' field,
        and the 'conversation' should have 'participants'.
        """
        return request.user in obj.conversation.participants.all()
