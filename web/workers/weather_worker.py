import data
import json

from web import web_worker


class WeatherWorker(web_worker.WebWorker):
    """Class to fetch information about the weather for a given location.
    
    Done using OpenWeatherMap.org.
    """
    def __init__(self, api_key):
        """
        Args:
            api_key (string): API key to use for OWM requests.
        """
        self.ttl = 600
        self._api_key = api_key

    def fetch(self, zip_code):
        """Retrieve weather information.

        Args:
            zip_code (string): Zip code to retrieve weather for.

        Returns (tuple):
            dict{string:string}: Current weather.
            list[dict{string:string}]: Forecasted weather (one item per day,
                starting with the current day).
        """
        geocode = data.geocodes[zip_code]
        url = ("https://api.openweathermap.org/data/2.5/onecall?"
               "lat={lat}&lon={lon}&exclude=minutely,hourly&appid={key}&"
               "units=imperial".format(lat=geocode["lat"],
                                       lon=geocode["lng"],
                                       key=self._api_key))
        weather = json.loads(self._make_request(url))
        return (weather["current"], weather["daily"])
