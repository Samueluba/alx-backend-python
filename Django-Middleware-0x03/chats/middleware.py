# chats/middleware.py

from datetime import datetime

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if hasattr(request, 'user') and request.user.is_authenticated else "Anonymous"
        with open("requests.log", "a") as log_file:
            log_file.write(f"{datetime.now()} - User: {user} - Path: {request.path}\n")
        response = self.get_response(request)
        return response

# Django-Middleware-0x03/chats/middleware.py

from datetime import datetime
from django.http import HttpResponseForbidden

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour

        # Allow access between 18 (6PM) and 21 (9PM)
        if not (18 <= current_hour < 21):
            return HttpResponseForbidden("Access is only allowed between 6PM and 9PM.")

        return self.get_response(request)
