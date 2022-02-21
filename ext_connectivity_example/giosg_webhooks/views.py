from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from . import serializers

from chat_app.models import ChatConversation, ChatMessage, Visitor

from giosg_api import api


class GiosgChatWebhookView(APIView):
    """
    APIs for handling chat webhooks from Giosg

    GET/POST /giosg_webhooks/chats
    """
    allowed_methods = ["POST", "GET"]

    def get(self, request, format=None):
        return Response({
            "detail": "Only POST requests supported. This endpoint is intended to be called by Giosg chat webhook"
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, *args, **kwargs):
        """
        Handle chat webhook from Giosg platform
        """
        # Printing to Django console for debug reasons
        print(request.body)

        serializer = serializers.ChatWebhookSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # We received chat state change webhook from Giosg.
            payload = serializer.validated_data
            resource_id = payload["resource_id"]

            if payload["action"] == "added":
                # If the action was "added" we need to create a new chat to
                # our third-party system.
                org_id = payload["resource"]["room_organization_id"]
                visitor_id = api.get_visitor_id(org_id, resource_id)

                try:
                    visitor = Visitor.objects.get(giosg_visitor_id=visitor_id)
                    chat = ChatConversation.objects.create(
                        giosg_chat_id=resource_id,
                        visitor=visitor,
                    )

                    print("Created", chat)
                except Visitor.DoesNotExist:
                    print("Visitor was not found so chat was not started by our app and we skip it")
            elif payload["action"] == "changed":
                # We dont care about changes at the moment but we could do something
                # with the changed information. One example could be to "end" the conversation when it
                # ends on Giosg platform.
                pass
            elif payload["action"] == "removed":
                # If the action was "removed" we can delete the chat from
                # our third-party chat system also. This could happen for example if data was asked to be
                # purged because of a GDPR reasons.
                try:
                    chat = ChatConversation.objects.get(giosg_chat_id=resource_id)
                    chat.delete()
                    print("Deleted", chat)
                except ChatConversation.DoesNotExist:
                    pass

            # We just return the data that we got in webhook payload.
            # We should respond with status code 2xx but the content could be empty.
            # This just helps debugging the webhooks.
            return Response(payload, status=status.HTTP_200_OK)


class GiosgChatMessageWebhookView(APIView):
    """
    APIs for handling chat webhooks from Giosg

    GET/POST /giosg_webhooks/messages
    """
    allowed_methods = ["POST", "GET"]

    def get(self, request, format=None):
        return Response({
            "detail": "Only POST requests supported. This endpoint is intended to be called by Giosg message webhook"
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, *args, **kwargs):
        """
        Handle message webhook from Giosg platform
        """
        # Printing to Django console for debug reasons
        print(request.body)

        serializer = serializers.MessageWebhookSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # We received chat message webhook from Giosg.
            payload = serializer.validated_data
            resource_id = payload["resource_id"]
            resource = payload["resource"]

            if payload["action"] == "added":
                # If the action was "added" we need to create a new message to
                # our third-party system.
                if resource["type"] == "msg":
                    # We ignore all other kinds of messages like join and leave notifications
                    # and care only about text content
                    sender_name = "Visitor" if resource["sender_type"] == "visitor" and resource["sender_name"] is None else resource["sender_name"]
                    message = ChatMessage.objects.create(
                        giosg_message_id=resource_id,
                        chat=ChatConversation.objects.get(giosg_chat_id=resource["chat_id"]),
                        sender_id=resource["sender_id"],
                        sender_name=sender_name,
                        message=resource["message"],
                    )

                    print("Created", message)
            elif payload["action"] == "changed":
                # We dont care about changes at the moment but we could do something
                # with the changed information
                pass
            elif payload["action"] == "removed":
                # If the action was "removed" we can delete the message from
                # our third-party chat system also.
                try:
                    message = ChatMessage.objects.get(giosg_id=resource_id)
                    message.delete()
                    print("Deleted", message)
                except ChatMessage.DoesNotExist:
                    pass

            # We just return the data that we got in webhook payload.
            # We should respond with status code 2xx but the content could be empty.
            # This just helps debugging the webhooks.
            return Response(payload, status=status.HTTP_200_OK)
