from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Message

@login_required
@cache_page(60)  # Cache this view for 60 seconds
def conversation_messages(request, conversation_id):
    # Example: Fetch messages in a conversation
    messages = Message.objects.filter(conversation_id=conversation_id).order_by('timestamp')

    return render(request, 'messaging/conversation.html', {'messages': messages})

