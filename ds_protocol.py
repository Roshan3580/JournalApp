# ROSHAN RAJ
# roshar1@uci.edu
# 90439894

# ds_protocol.py

import json
from typing import Union, Dict, List
from collections import namedtuple


DataTuple = namedtuple('DataTuple', ['token', 'join', 'post', 'bio', 'response'])


def extract_json(json_msg: str) -> DataTuple:
    """
    Extracts information from a JSON-formatted message.

    Args:
        json_msg (str): The JSON-formatted message.

    Returns:
        DataTuple: A namedtuple containing token, join, post, bio, and response fields.
    """
    try:
        json_obj = json.loads(json_msg)
        return DataTuple(
            json_obj.get('token', ''),
            json_obj.get('join', {}),
            json_obj.get('post', {}),
            json_obj.get('bio', {}),
            json_obj.get('response', {})
        )
    except json.JSONDecodeError:
        print("JSON cannot be decoded.")


def create_join_message(username: str, password: str, token: str = "") -> str:
    """
    Creates a JSON-formatted join message.

    Args:
        username (str): The username for joining.
        password (str): The password for joining.
        token (str, optional): The token. Defaults to "".

    Returns:
        str: The JSON-formatted join message.
    """
    message = {"join": {"username": username, "password": password, "token": token}}
    return json.dumps(message)


def create_post_message(token: str, entry: str, timestamp: str) -> str:
    """
    Creates a JSON-formatted post message.

    Args:
        token (str): The token.
        entry (str): The entry content.
        timestamp (str): The timestamp.

    Returns:
        str: The JSON-formatted post message.
    """
    message = {"token": token, "post": {"entry": entry, "timestamp": timestamp}}
    return json.dumps(message)


def create_bio_message(token: str, entry: str, timestamp: str) -> str:
    """
    Creates a JSON-formatted bio message.

    Args:
        token (str): The token.
        entry (str): The entry content.
        timestamp (str): The timestamp.

    Returns:
        str: The JSON-formatted bio message.
    """
    message = {"token": token, "bio": {"entry": entry, "timestamp": timestamp}}
    return json.dumps(message)


def process_response(response: Union[Dict, str]) -> str:
    """
    Processes the response received from the server.

    Args:
        response (Union[Dict, str]): The response received from the server.

    Returns:
        str: A processed response message.
    """
    if isinstance(response, str):
        try:
            response_dict = json.loads(response)
            response_type = response_dict.get("response", {}).get("type", "")
            message = response_dict.get("response", {}).get("message", "")
            token = response_dict.get("response", {}).get("token", "")

            if response_type == "ok":
                return f"OK: {message}, Token: {token}"
            elif response_type == "error":
                return f"Error: {message}"
            else:
                return "Unknown response type"
        except json.JSONDecodeError:
            return "Invalid JSON in response"
    else:
        return "Invalid response format"


def process_direct_message_response(response: Union[Dict, str]) -> Union[str, List[Dict]]:
    """
    Processes the direct message response received from the server.

    Args:
        response (Union[Dict, str]): The direct message response received from the server.

    Returns:
        Union[str, List[Dict]]: A processed response message or a list of direct messages.
    """
    if isinstance(response, str):
        try:
            response_dict = json.loads(response)
            response_type = response_dict.get("response", {}).get("type", "")
            message = response_dict.get("response", {}).get("message", "")
            token = response_dict.get("response", {}).get("token", "")

            if response_type == "ok":
                if "messages" in response_dict.get("response", {}):
                    return response_dict.get("response", {}).get("messages", [])
                else:
                    return f"OK: {message}, Token: {token}"
            elif response_type == "error":
                return f"Error: {message}"
            else:
                return "Unknown response type"
        except json.JSONDecodeError:
            return "Invalid JSON in response"
    else:
        return "Invalid response format"


def create_direct_message(token: str, entry: str, recipient: str, timestamp: str) -> str:
    """
    Creates a JSON-formatted direct message.

    Args:
        token (str): The token.
        entry (str): The entry content.
        recipient (str): The recipient's username.
        timestamp (str): The timestamp.

    Returns:
        str: The JSON-formatted direct message.
    """
    message = {"token": token, "directmessage": {"entry": entry, "recipient": recipient, "timestamp": timestamp}}
    return json.dumps(message)


def request_direct_messages(token: str, request_type: str = "new") -> str:
    """
    Creates a JSON-formatted request for direct messages.

    Args:
        token (str): The token.
        request_type (str, optional): The request type, either "new" or "all". Defaults to "new".

    Returns:
        str: The JSON-formatted request message for direct messages.
    """
    message = {"token": token, "directmessage": request_type}
    return json.dumps(message)


def request_all_direct_messages(token: str, request_type: str = "all") -> str:
    """
    Creates a JSON-formatted request for all direct messages.

    Args:
        token (str): The token.
        request_type (str, optional): The request type, either "new" or "all". Defaults to "all".

    Returns:
        str: The JSON-formatted request message for all direct messages.
    """
    message = {"token": token, "directmessage": request_type}
    return json.dumps(message)
