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
