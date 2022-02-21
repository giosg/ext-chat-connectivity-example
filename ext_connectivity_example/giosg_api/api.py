import requests
import json
from django.conf import settings
from django.core.cache import cache


def _set_visitor_token_to_cache(visitor):
    """
    Helper for storing visitor access token in local cache
    """
    visitor_id = visitor["visitor_id"]
    visitor_token = visitor["access_token"]
    cache_ttl = int(visitor["expires_in"]) - 10
    cache.set(f"access_token_{visitor_id}", visitor_token, cache_ttl)


def get_access_token_for_visitor(organization_id, visitor_id, visitor_secret_id, visitor_global_id):
    """
    Returns visitor access token from local cache or authenticates against Giosg server if not found
    """
    token = cache.get(f"access_token_{visitor_id}")
    if not token:
        visitor = authenticate_giosg_visitor(organization_id, visitor_secret_id, visitor_global_id)
        return visitor["access_token"]
    return token


def create_giosg_visitor(organization_id, room_id):
    """
    Creates new Giosg visitor and assigns that visitor into a room
    """
    # See: https://docs.giosg.com/api_reference/giosg_live/giosg_public_http_api/general/#authenticate-a-new-visitor
    visitor_auth_url = f"https://service.giosg.com/api/v5/public/orgs/{organization_id}/auth"
    auth_payload = {
        "visitor_secret_id": None,
        "visitor_global_id": None
    }
    auth_response = requests.post(visitor_auth_url, data=json.dumps(auth_payload), headers={
        "Content-Type": "application/json",
    })
    auth_response.raise_for_status()
    visitor = auth_response.json()

    visitor_id = visitor["visitor_id"]
    visitor_token = visitor["access_token"]
    _set_visitor_token_to_cache(visitor)

    # See: https://docs.giosg.com/api_reference/giosg_live/giosg_public_http_api/visitors/#create-a-new-room-visitor
    visitor_api_url = f"https://service.giosg.com/api/v5/public/orgs/{organization_id}/rooms/{room_id}/visitors"
    visitor_response = requests.post(visitor_api_url, data=json.dumps({"id": visitor_id}), headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {visitor_token}"
    })
    visitor_response.raise_for_status()

    return visitor


def authenticate_giosg_visitor(organization_id, visitor_secret_id, visitor_global_id):
    """
    Authenticates existing Giosg visitors against Giosg servers
    """
    # See: https://docs.giosg.com/api_reference/giosg_live/giosg_public_http_api/general/#authenticate-a-new-visitor
    visitor_auth_url = f"https://service.giosg.com/api/v5/public/orgs/{organization_id}/auth"
    auth_payload = {
        "visitor_secret_id": visitor_secret_id,
        "visitor_global_id": visitor_global_id
    }
    auth_response = requests.post(visitor_auth_url, data=json.dumps(auth_payload), headers={
        "Content-Type": "application/json",
    })
    auth_response.raise_for_status()
    visitor = auth_response.json()
    _set_visitor_token_to_cache(visitor)

    return visitor


def set_visitor_name(organization_id, room_id, visitor_id, visitor_name):
    """
    Set visitors name
    """
    # Add name for the visitor
    # See: https://docs.giosg.com/api_reference/giosg_live/giosg_http_api/visitors/#room-visitor-variables
    visitor_variable_url = f"https://service.giosg.com/api/v5/orgs/{organization_id}/rooms/{room_id}/visitors/{visitor_id}/variables"
    variable_response = requests.post(visitor_variable_url, data=json.dumps({"key": "username", "value": visitor_name}), headers={
        "Content-Type": "application/json",
        "Authorization": f"Token {settings.GIOSG_API_TOKEN}"
    })
    variable_response.raise_for_status()
    return variable_response.json()


def create_new_chat_as_visitor(organization_id, room_id, visitor_id, access_token):
    """
    Create a new chat as a visitor to Giosg platform
    """
    # https://docs.giosg.com/api_reference/giosg_live/giosg_public_http_api/chats/#create-a-new-chat
    chat_api_url = f"https://service.giosg.com/api/v5/public/orgs/{organization_id}/rooms/{room_id}/visitors/{visitor_id}/chats"
    chat_response = requests.post(chat_api_url, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    })
    try:
        chat_response.raise_for_status()
    except requests.HTTPError as ex:
        print("Failed to create new visitor chat:", chat_response.content)
        raise ex
    return chat_response.json()


def send_message_as_visitor(visitor_id, chat_id, access_token, message):
    """
    Send a message to existing chat
    """
    api_url = f"https://service.giosg.com/api/v5/public/visitors/{visitor_id}/chats/{chat_id}/messages"
    payload = {
        "type": "msg",
        "message": message
    }
    msg_response = requests.post(api_url, json.dumps(payload), headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    })
    msg_response.raise_for_status()
    return msg_response.json()


def get_visitor_id(organization_id, chat_id):
    """
    Get visitor_id from chat memberships
    """
    # See: https://docs.giosg.com/api_reference/giosg_live/giosg_http_api/chats/#chat-memberships
    api_url = f"https://service.giosg.com/api/v5/orgs/{organization_id}/owned_chats/{chat_id}/memberships"
    response = requests.get(api_url, headers={
        "Content-Type": "application/json",
        "Authorization": f"Token {settings.GIOSG_API_TOKEN}",
    })
    response.raise_for_status()
    memberships = response.json()["results"]

    try:
        visitor_member = next(filter(lambda m: m["member_type"] == "visitor", memberships))
        return visitor_member["member_id"]
    except StopIteration:
        return None
