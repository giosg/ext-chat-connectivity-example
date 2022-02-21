from django.urls import path
from .views import GiosgChatWebhookView, GiosgChatMessageWebhookView


urlpatterns = [
    path('giosg_webhooks/chats', GiosgChatWebhookView.as_view(), name='giosg_chat_webhook'),
    path('giosg_webhooks/messages', GiosgChatMessageWebhookView.as_view(), name='giosg_message_webhook'),
]
