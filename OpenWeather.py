from WebAPI import WebAPI


class OpenWeather(WebAPI):
    """
    A class representing OpenWeather API.

    Attributes:
        zipcode (str): The ZIP code.
        ccode (str): The country code.
        temperature (float): The current temperature.
        high_temperature (float): The high temperature.
        low_temperature (float): The low temperature.
        longitude (float): The longitude.
        latitude (float): The latitude.
        description (str): The weather description.
        humidity (int): The humidity percentage.
        sunset (int): The sunset time.
        city (str): The city name.

    Methods:
        load_data: Loads weather data from the OpenWeather API.
        transclude: Replaces "@weather" in a message with the current temperature.

    Inherits from:
        WebAPI
    """
    def __init__(self, zipcode: str, ccode: str):
        super().__init__()
        self.zipcode = zipcode
        self.ccode = ccode
        self.temperature = None
        self.high_temperature = None
        self.low_temperature = None
        self.longitude = None
        self.latitude = None
        self.description = None
        self.humidity = None
        self.sunset = None
        self.city = None


    def load_data(self) -> None:
        try:
            if self.apikey is None:
                raise ValueError("API key is not set. Use set_apikey method to set the API key.")

            url = f"http://api.openweathermap.org/data/2.5/weather?zip={self.zipcode},{self.ccode}&appid={self.apikey}"

            response = self._download_url(url)

            self.temperature = response['main']['temp']
            self.high_temperature = response['main']['temp_max']
            self.low_temperature = response['main']['temp_min']
            self.longitude = response['coord']['lon']
            self.latitude = response['coord']['lat']
            self.description = response['weather'][0]['description']
            self.humidity = response['main']['humidity']
            self.sunset = response['sys']['sunset']
            self.city = response['name']

        except ValueError as v:
            print(f"ValueError: {v}")
        except KeyError as k:
            print(f"KeyError: {k}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


    def transclude(self, message: str) -> str:
        return message.replace("@weather", str(self.temperature))
