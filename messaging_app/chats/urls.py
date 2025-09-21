from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from conversations.views import ConversationViewSet, MessageViewSet  # import your viewsets

# Create a router and register your viewsets
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('admin/', admin.site.urls),
    # Include API routes with prefix 'api/'
    path('api/', include(router.urls)),
]

