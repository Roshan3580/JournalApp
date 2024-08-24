# ROSHAN RAJ
# 90439894
# roshar1@uci.edu

# ds_messenger.py

import socket
from ds_protocol import create_join_message, extract_json, create_direct_message
from ds_protocol import request_all_direct_messages, request_direct_messages
from typing import List
from collections import namedtuple
import time

DataTuple = namedtuple('DataTuple', ['token', 'directmessage', 'response'])


class DirectMessage:
    def __init__(self):
        self.recipient = None
        self.message = None
        self.timestamp = None


class DirectMessenger:
    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None
        self.server = dsuserver
        self.port = 3021
        self.username = username
        self.password = password
        self.your_user_token = None

    def send(self, message: str, recipient: str) -> bool:
        """
        Send a direct message to a recipient.

        Args:
            message (str): The message to be sent.
            recipient (str): The recipient's username.

        Returns:
            bool: True if the message is sent successfully, False otherwise.
        """

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv:
                serv.connect((self.server, self.port))

                serv_input = serv.makefile('r')
                serv_output = serv.makefile('w')

                if not self.your_user_token:
                    join_message = create_join_message(self.username, self.password, "")
                    serv_output.write(join_message + "\r\n")
                    serv_output.flush()

                    response = serv_input.readline()[:-1]
                    data = extract_json(response)
                    if data.response.get('type') == "ok":
                        self.your_user_token = data.response.get('token')
                    else:
                        print(f"Failed to join: {data.response.get('message')}")
                        return False

                if message:
                    json_message = create_direct_message(self.your_user_token, message, recipient, str(time.time()))

                serv_output.write(json_message + "\r\n")
                serv_output.flush()

                response = serv_input.readline()[:-1]
                data = extract_json(response)
                if data.response.get('type') == "ok":
                    print("Message sent successfully!")
                    return True
                else:
                    print(f"Failed to send message: {data.response.get('message')}")
                    return False
        except Exception as e:
            print(f"Error: {e}")
            return False

    def retrieve_new(self) -> List[DirectMessage]:
        """
        Retrieve new direct messages.

        Returns:
            List[DirectMessage]: A list of DirectMessage objects representing the new messages.
        """

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv:
                serv.connect((self.server, self.port))

                serv_input = serv.makefile('r')
                serv_output = serv.makefile('w')

                if not self.your_user_token:
                    join_message = create_join_message(self.username, self.password, "")
                    serv_output.write(join_message + "\r\n")
                    serv_output.flush()

                    response = serv_input.readline()[:-1]
                    data = extract_json(response)
                    if data.response.get('type') == "ok":
                        self.your_user_token = data.response.get('token')
                    else:
                        print(f"Failed to join: {data.response.get('message')}")
                        return []

                request_message = request_direct_messages(self.your_user_token, "new")
                serv_output.write(request_message + "\r\n")
                serv_output.flush()

                response = serv_input.readline()[:-1]
                data = extract_json(response)
                if data.response.get('type') == "ok":
                    messages = data.response.get('messages', [])
                    direct_messages = []
                    for msg in messages:
                        direct_message = DirectMessage()
                        direct_message.recipient = msg.get('from')
                        direct_message.message = msg.get('message')
                        direct_message.timestamp = msg.get('timestamp')
                        direct_messages.append(direct_message)
                    return direct_messages
                else:
                    print(f"Failed to retrieve new messages: {data.response.get('message')}")
                    return []
        except Exception as e:
            print(f"Error: {e}")
            return []

    def retrieve_all(self) -> List[DirectMessage]:
        """
        Retrieve all direct messages.

        Returns:
            List[DirectMessage]: A list of DirectMessage objects representing all messages.
        """

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv:
                serv.connect((self.server, self.port))

                serv_input = serv.makefile('r')
                serv_output = serv.makefile('w')


                if not self.your_user_token:
                    join_message = create_join_message(self.username, self.password, "")
                    serv_output.write(join_message + "\r\n")
                    serv_output.flush()

                    response = serv_input.readline()[:-1]
                    data = extract_json(response)
                    if data.response.get('type') == "ok":
                        self.your_user_token = data.response.get('token')
                    else:
                        print(f"Failed to join: {data.response.get('message')}")
                        return []

                request_message = request_all_direct_messages(self.your_user_token, "all")
                serv_output.write(request_message + "\r\n")
                serv_output.flush()

                response = serv_input.readline()[:-1]
                data = extract_json(response)
                if data.response.get('type') == "ok":
                    messages = data.response.get('messages', [])
                    direct_messages = []
                    for msg in messages:
                        direct_message = DirectMessage()
                        direct_message.recipient = msg.get('from')
                        direct_message.message = msg.get('message')
                        direct_message.timestamp = msg.get('timestamp')
                        direct_messages.append(direct_message)
                    return direct_messages
                else:
                    print(f"Failed to retrieve all messages: {data.response.get('message')}")
                    return []
        except Exception as e:
            print(f"Error: {e}")
            return []
