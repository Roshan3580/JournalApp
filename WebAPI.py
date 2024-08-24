# ROSHAN RAJ
# 90439894
# roshar1@uci.edu

# WebAPI.py

from abc import ABC, abstractmethod
import urllib.request
import json
from urllib import error


class WebAPI(ABC):
    def __init__(self):
        self.apikey = None


    def _download_url(self, url: str) -> dict:
        try:
            response = urllib.request.urlopen(url)
            json_results = response.read()
            result = json.loads(json_results)
        except urllib.error.HTTPError as e:
            print(f"HTTP Error: {e.code}")
            result = {}
        except urllib.error.URLError as e:
            print(f"Failed to connect to the API. Error: {e}")
            result = {}
        except json.JSONDecodeError:
            print("Invalid data formatting from the API.")
            result = {}
        finally:
            if response is not None:
                response.close()

        return result


    def set_apikey(self, apikey: str) -> None:
        self.apikey = apikey


    @abstractmethod
    def load_data(self):
        pass


    @abstractmethod
    def transclude(self, message: str) -> str:
        pass
