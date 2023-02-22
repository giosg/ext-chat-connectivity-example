from django.db import models
import uuid


class Visitor(models.Model):
    """
    Model for storing information about Giosg visitors. This could link one-to-one to our third-party
    application user.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    giosg_visitor_id = models.CharField(max_length=256)
    giosg_visitor_secret_id = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    visitor_name = models.CharField(unique=True, max_length=256)


class ChatConversation(models.Model):
    """
    Model for storing information about chat conversations. Basically connects "giosg_chat_id"
    into a "visitor" model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    giosg_chat_id = models.CharField(max_length=256, unique=True)
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class ChatMessage(models.Model):
    """
    Model for storing chat messages which belong to a "chat"
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat = models.ForeignKey(ChatConversation, null=True, on_delete=models.CASCADE)
    giosg_message_id = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    sender_id = models.CharField(max_length=256)
    sender_name = models.CharField(max_length=256)
    message = models.CharField(max_length=2048)
