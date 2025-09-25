# messaging_app/chats/auth.py

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions

class CustomJWTAuthentication(JWTAuthentication):
    """
    You can extend this if you want additional checks or token validation logic.
    """

    def authenticate(self, request):
        # This calls the base class's authenticate to get (user, token)
        user_token = super().authenticate(request)
        if user_token is None:
            return None
        user, token = user_token

        # Optionally add custom checks here (e.g. user.is_active)
        if not user.is_active:
            raise exceptions.AuthenticationFailed("User account is disabled.", code='user_inactive')

        return user, token
