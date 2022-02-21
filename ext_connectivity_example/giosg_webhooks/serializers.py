from rest_framework import serializers


class ChatSerializer(serializers.Serializer):
    """
    Serializer for chat webhook payload.
    See https://docs.giosg.com/api_reference/giosg_live/giosg_http_api/chats/

    Note that webhooks only receive changes if the "action" in webhook payload is "changed".
    A full resource is included if the "action" is "added".

    Also note that this example also omits handling many fields available in the resource as
    we are not interested about them in this example.
    """
    id = serializers.CharField(max_length=200, required=False)
    chat_type = serializers.CharField(max_length=200, required=False)
    room_id = serializers.CharField(max_length=200, required=False)
    room_organization_id = serializers.CharField(max_length=200, required=False)
    room_name = serializers.CharField(max_length=200, required=False)
    tag_count = serializers.IntegerField(required=False)
    message_count = serializers.IntegerField(required=False)
    user_message_count = serializers.IntegerField(required=False)
    visitor_message_count = serializers.IntegerField(required=False)
    has_messages = serializers.BooleanField(required=False)
    has_user_messages = serializers.BooleanField(required=False)
    has_visitor_messages = serializers.BooleanField(required=False)
    present_participant_count = serializers.IntegerField(required=False)
    present_user_participant_count = serializers.IntegerField(required=False)
    present_visitor_participant_count = serializers.IntegerField(required=False)
    member_count = serializers.IntegerField(required=False)
    user_member_count = serializers.IntegerField(required=False)
    visitor_member_count = serializers.IntegerField(required=False)
    is_private = serializers.BooleanField(required=False)
    is_real_conversation = serializers.BooleanField(required=False)
    is_autosuggested = serializers.BooleanField(required=False)
    is_waiting = serializers.BooleanField(required=False)
    is_pending = serializers.BooleanField(required=False)
    is_ended = serializers.BooleanField(required=False)
    is_encrypted = serializers.BooleanField(required=False)


class ChatWebhookSerializer(serializers.Serializer):
    """
    Serializer for chat webhook.

    Field "action" can be "added", "changed" or "removed".
    Field "resource_id" is the chat conversation ID this webhook originates from.
    Field "resource" contains the actual chat resource data
    Field "channel" contains the path of the resource
    """
    action = serializers.CharField(max_length=50)
    resource_id = serializers.CharField(max_length=50)
    resource = ChatSerializer()
    channel = serializers.CharField(max_length=256)


class AvatarSerializer(serializers.Serializer):
    """
    Nested serializer for sender avatar image
    """
    id = serializers.CharField(max_length=50, required=False)
    url = serializers.CharField(max_length=2048, required=False)


class MessageSerializer(serializers.Serializer):
    """
    Serializer for message webhook payload.
    See https://docs.giosg.com/api_reference/giosg_live/giosg_http_api/chats/#chat-messages

    Note that webhooks only receive changes if the "action" in webhook payload is "changed".
    A full resource is included if the "action" is "added".

    Also note that this example also omits handling many fields available in the resource as
    we are not interested about them in this example.
    """

    id = serializers.CharField(max_length=50, required=False)
    type = serializers.CharField(max_length=20, required=False)
    chat_id = serializers.CharField(max_length=50, required=False)
    room_id = serializers.CharField(max_length=50, required=False)

    sender_type = serializers.CharField(max_length=50, required=False)
    sender_id = serializers.CharField(max_length=50, required=False)
    sender_public_name = serializers.CharField(max_length=200, required=False, allow_null=True)
    sender_name = serializers.CharField(max_length=200, required=False, allow_null=True)
    sender_avatar = AvatarSerializer(required=False, allow_null=True)
    message = serializers.CharField(max_length=2048, required=False, allow_null=True)
    is_encrypted = serializers.BooleanField(required=False)


class MessageWebhookSerializer(serializers.Serializer):
    """
    Serializer for message webhook.

    Field "action" can be "added", "changed" or "removed".
    Field "resource_id" is the chat message ID this webhook originates from.
    Field "resource" contains the actual message resource data
    Field "channel" contains the path of the resource
    """
    action = serializers.CharField(max_length=50)
    resource_id = serializers.CharField(max_length=50)
    resource = MessageSerializer()
    channel = serializers.CharField(max_length=256)
