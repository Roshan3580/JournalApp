# ROSHAN RAJ
# 90439894
# roshar1@uci.edu

# LastFM.py

from WebAPI import WebAPI

class LastFM(WebAPI):
    """
    A class representing LastFM API.

    Attributes:
        user (str): The LastFM user.
        top_tracks (list): The top tracks of the user.
        artist_info (dict): Information about the artist.
        artist_name (str): The name of the artist.

    Methods:
        load_data: Loads artist information from the LastFM API.
        get_top_tracks: Retrieves the top tracks of the user from the LastFM API.
        transclude: Replaces "@lastfm" in a message with the number of listeners of the artist.

    Inherits from:
        WebAPI
    """
    def __init__(self, user, artist_name):
        super().__init__()
        self.user = user
        self.top_tracks = []
        self.artist_info = {}
        self.artist_name = artist_name.strip().replace(" ", "+")


    def load_data(self) -> None:
        if self.apikey is None:
            raise ValueError("API key is not set. Use set_apikey method to set the Last.FM API key.")

        url = f"http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={self.artist_name}&api_key={self.apikey}&format=json"

        try:
            response = self._download_url(url)
            artist_obj = response.get('artist', {})

            self.artist_info = artist_obj

        except ValueError as v:
            print(f"ValueError: {v}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


    def get_top_tracks(self) -> None:
        if self.apikey is None:
            raise ValueError("API key is not set. Use set_apikey method to set the Last.FM API key.")

        url = f"http://ws.audioscrobbler.com/2.0/?method=user.gettoptracks&user={self.user}&api_key={self.apikey}&format=json"

        try:
            response = self._download_url(url)
            tracks_obj = response.get('toptracks', {})
            self.top_tracks = tracks_obj.get('track', [])

        except ValueError as v:
            print(f"ValueError: {v}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


    def transclude(self, message: str) -> str:
        return message.replace("@lastfm", str(self.artist_info.get('stats', {}).get('listeners')))
