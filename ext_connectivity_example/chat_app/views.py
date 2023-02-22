from django.views.generic import TemplateView
from django.conf import settings
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from . import models
from . import serializers

from giosg_api import api


class ChatView(TemplateView):
    """
    Template view for displaying our simple chat app at /chat-app url.

    GET /chat-app
    """
    template_name = "chat.html"


class ChatConversationViewSet(viewsets.ModelViewSet):
    """
    APIs for listing, updating, retrieving and creating chat conversations.

    GET/PUT/PATCH/POST/DELETE /api/chats
    """
    serializer_class = serializers.ChatConversationSerializer
    queryset = models.ChatConversation.objects.all()

    def create(self, request, *args, **kwargs):
        """
        When new chat gets POSTed, we first send it to Giosg as we can then get it
        back with webhook and add it to our own database
        """
        serializer = serializers.ChatConversationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        try:
            local_visitor = models.Visitor.objects.get(visitor_name=serializer.validated_data["visitor_name"])
            visitor_secret_id = local_visitor.giosg_visitor_secret_id
            visitor_id = local_visitor.giosg_visitor_id
            access_token = api.get_access_token_for_visitor(settings.GIOSG_ORGANIZATION_ID, visitor_id, visitor_secret_id)
        except models.Visitor.DoesNotExist:
            # Visitor was not found so lets create a new one
            visitor = api.create_giosg_visitor(settings.GIOSG_ORGANIZATION_ID, settings.GIOSG_ROOM_ID)
            visitor_id = visitor["visitor_id"]
            visitor_secret_id = visitor["visitor_secret_id"]
            access_token = visitor["access_token"]

            # Store giosg visitor informatio to our app also
            local_visitor = models.Visitor.objects.create(
                giosg_visitor_id=visitor_id,
                giosg_visitor_secret_id=visitor_secret_id,
                visitor_name=serializer.validated_data["visitor_name"]
            )

        # Always update visitors name
        api.set_visitor_name(settings.GIOSG_ORGANIZATION_ID, settings.GIOSG_ROOM_ID, visitor_id, serializer.validated_data["visitor_name"])

        # Start new chat
        chat_response = api.create_new_chat_as_visitor(settings.GIOSG_ORGANIZATION_ID, settings.GIOSG_ROOM_ID, visitor_id, access_token)
        # NOTE: We could create the ChatConversation object to our local database here but it is not needed as
        # we get it back as a webook, we then handle all messages in same place.
        # models.ChatConversation.objects.create(
        #     giosg_chat_id=chat_response["id"],
        #     visitor=local_visitor,
        # )

        return chat_response


class ChatMessageViewSet(viewsets.ModelViewSet):
    """
    APIs for listing, updating, retrieving and creating chat messages.

    GET/PUT/PATCH/POST/DELETE /api/chats/<chat_id>/messages
    """
    serializer_class = serializers.ChatMessageSerializer

    def get_queryset(self):
        return models.ChatMessage.objects.filter(chat_id=self.kwargs["chat_id"])

    def create(self, request, *args, **kwargs):
        """
        When new message gets POSTed, we first send it to Giosg as we can then get it
        back with webhook and add it to our own database
        """
        serializer = serializers.ChatMessageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        chat_id = self.kwargs["chat_id"]
        chat = models.ChatConversation.objects.get(id=chat_id)
        visitor_id = chat.visitor.giosg_visitor_id
        visitor_token = api.get_access_token_for_visitor(
            settings.GIOSG_ORGANIZATION_ID,
            visitor_id,
            chat.visitor.giosg_visitor_secret_id,
        )
        msg_data = api.send_message_as_visitor(visitor_id, chat.giosg_chat_id, visitor_token, serializer.validated_data["message"])

        # NOTE: We could create the ChatMessage object to our local database here but it is not needed as
        # we get it back as a webook, we then handle all messages in same place.
        # models.ChatMessage.objects.create(
        #     chat=chat,
        #     giosg_message_id=msg_data["id"],
        #     sender_id=msg_data["sender_id"],
        #     sender_name="You",
        #     message=msg_data["message"],
        # )
