from django.urls import path
from rest_framework import routers

from .views import ChatConversationViewSet, ChatMessageViewSet, ChatView

router = routers.SimpleRouter()
router.register(r'api/chats', ChatConversationViewSet)
router.register(r"api/chats/(?P<chat_id>[\w-]+)/messages", ChatMessageViewSet, basename="chat-messages")


urlpatterns = [
    path('chat-app/', ChatView.as_view()),
]

urlpatterns += router.urls
