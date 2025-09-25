from rest_framework import permissions
from rest_framework.permissions import BasePermission


# chats/permissions.py

from rest_framework import permissions
from rest_framework.permissions import BasePermission

class IsParticipant(BasePermission):
    """
    Custom permission to allow only participants of a conversation or message.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user

        # If object has a 'participants' field (ManyToMany)
        if hasattr(obj, 'participants'):
            return user in obj.participants.all()

        # If object has 'sender' and 'receiver' fields
        if hasattr(obj, 'sender') and hasattr(obj, 'receiver'):
            return obj.sender == user or obj.receiver == user

        return False
