from rest_framework import serializers
from . import models


class ChatConversationSerializer(serializers.ModelSerializer):
    """
    Serializer used when listing chat conversations
    """
    visitor_name = serializers.SerializerMethodField()

    class Meta:
        model = models.ChatConversation
        fields = "__all__"

    def get_visitor_name(self, obj):
        return obj.visitor.visitor_name


class ChatConversationCreateSerializer(serializers.Serializer):
    """
    Serializer used when creating chat conversations
    """
    visitor_name = serializers.CharField(max_length=256)


class ChatMessageSerializer(serializers.ModelSerializer):
    """
    Serializer used when listing chat messages
    """
    class Meta:
        model = models.ChatMessage
        fields = "__all__"


class ChatMessageCreateSerializer(serializers.Serializer):
    """
    Serializer used when creating chat messages
    """
    message = serializers.CharField(max_length=2048)
