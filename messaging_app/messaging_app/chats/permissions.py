from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to authenticated users who are participants of the conversation.
    """

    def has_permission(self, request, view):
        # Explicitly check if the user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        """
        Check if the authenticated user is a participant of the conversation.
        Assumes obj is a Message instance with obj.conversation.participants.
        """
        return request.user in obj.conversation.participants.all()

