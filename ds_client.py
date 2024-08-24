# ROSHAN RAJ
# 90439894
# roshar1@uci.edu

# ds_client.py

import socket
from ds_protocol import extract_json, create_join_message, create_post_message, create_bio_message
from LastFM import LastFM
from OpenWeather import OpenWeather
import time


def send(server: str, port: int, username: str, password: str, message: str, bio: str = None):
    """
    Send a message to the designated server.

    Args:
        server (str): The server address.
        port (int): The port number.
        username (str): The username.
        password (str): The password.
        message (str): The message to be sent.
        bio (str, optional): The bio to be included. Defaults to None.

    Returns:
        bool: True if the message is sent successfully, False otherwise.
    """

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv:
            serv.connect((server, port))

            serv_input = serv.makefile('r')
            serv_output = serv.makefile('w')

            print(f"Connected to {server} (port {port})")

            if "your_user_token" not in globals():
                join_message = create_join_message(username, password, "")
                serv_output.write(join_message + "\r\n")
                serv_output.flush()

                response = serv_input.readline()[:-1]
                data = extract_json(response)
                if data.response.get('type') == "ok":
                    global your_user_token
                    your_user_token = data.response.get('token')
                else:
                    print(f"Failed to join: {data.response.get('message')}")
                    return False

            if "@lastfm" in message:
                apikey = "8020b6e072d7a629b29caf7adb3c62f6"
                user_name = "roshar1"
                artist_name = "Kanye West"
                last_fm = LastFM(user_name, artist_name)
                last_fm.set_apikey(apikey)
                last_fm.load_data()
                message = last_fm.transclude(message)

            if "@weather" in message:
                zipcode = "92697"
                ccode = "US"
                apikey = "f845b730501e322e7835c1c680f477b2"
                open_weather = OpenWeather(zipcode, ccode)
                open_weather.set_apikey(apikey)
                open_weather.load_data()
                message = open_weather.transclude(message)

            if message:
                json_message = create_post_message(your_user_token, message, str(time.time()))
            elif bio:
                json_message = create_bio_message(your_user_token, bio, str(time.time()))
            else:
                print("No message or bio to send.")
                return False

            serv_output.write(json_message + "\r\n")
            serv_output.flush()

            response = serv_input.readline()[:-1]
            print(f"Response: {response}")
            print(f"Post added successfully!")

            serv_input.close()
            serv_output.close()
            serv.close()
            return True
    except Exception as e:
        print(f"Error: {e}")
        return False
