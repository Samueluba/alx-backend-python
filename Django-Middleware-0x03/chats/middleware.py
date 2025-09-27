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

# Django-Middleware-0x03/chats/middleware.py

import time
from django.http import HttpResponseForbidden

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_log = {}  # {ip_address: [timestamps]}

    def __call__(self, request):
        if request.method == 'POST':
            ip = self.get_client_ip(request)
            now = time.time()

            # Keep only timestamps from the last 60 seconds
            timestamps = self.message_log.get(ip, [])
            timestamps = [ts for ts in timestamps if now - ts < 60]

            if len(timestamps) >= 5:
                return HttpResponseForbidden("Message limit exceeded: Max 5 messages per minute.")

            # Add current timestamp and save
            timestamps.append(now)
            self.message_log[ip] = timestamps

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')

