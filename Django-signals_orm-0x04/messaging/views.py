from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.models import User

@login_required
def delete_user(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('account_deleted')  # Or another appropriate URL
    return render(request, 'confirm_delete.html')

from django.shortcuts import render, get_object_or_404
from .models import Message

# ✅ Efficient top-level conversation view
def conversation_list_view(request):
    """
    Shows top-level messages (parent_message is null) and prefetches replies.
    """
    messages = Message.objects.filter(parent_message__isnull=True) \
        .select_related('sender', 'receiver') \
        .prefetch_related('replies__sender', 'replies__receiver') \
        .order_by('-timestamp')

    return render(request, 'messaging/conversation_list.html', {
        'messages': messages
    })


# ✅ Recursive query builder
def build_thread(message):
    return {
        'message': message,
        'replies': [build_thread(reply) for reply in message.replies.all().order_by('timestamp')]
    }


# ✅ Recursive threaded conversation view
def threaded_conversation_view(request, message_id):
    root = get_object_or_404(
        Message.objects.select_related('sender', 'receiver')
        .prefetch_related('replies__sender', 'replies__receiver'),
        id=message_id
    )

    thread = build_thread(root)

    return render(request, 'messaging/threaded_conversation.html', {
        'thread': thread
    })


