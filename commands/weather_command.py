from commands.core import base_command
from web import web_worker
from urllib import request

import json
import re

_zip_code_re = re.compile(r'\d{5}')


class WeatherCommand(base_command.BaseCommand):
    """Class to add 'weather' command to bot."""
    @classmethod
    def trigger_word(cls):
        return "weather"

    def __init__(self, api_key):
        """Prepare an instance to query `OpenWeatherMap.org`.

        Args:
            api_key (string): API key to use for OWM requests.
        """
        self._api_key = api_key

    def list_conditions(self, conditions):
        """Generate a string listing the given conditions.

        E.g. ["smoke", "clouds", "fog"] -> "smoke, clouds, and fog"

        Args:
            conditions (list[dict{string:string}]): Conditions to list. These
                are expected to come from OpenWeatherMap, so it should be a list
                of dicts that have a "description" entry.

        Returns:
            (string) The conditions in a human-readable list.
        """
        descriptions = [condition["description"] for condition in conditions]
        return ", and ".join(
            filter(None, [", ".join(descriptions[:-1]), *descriptions[-1:]]))

    def build_message(self, zip, city, current_weather, daily_forecast):
        """Build the message about weather to send to Discord.

        Args:
            zip (string): Zip code weather was requested for.
            city (string): City name that the given zip maps to.
            current_weather (dict{string:string}): Parsed from OpenWeatherMap.
            daily_forecast (dict{string:string}): Parsed from OpenWeatherMap.
        """
        return (
            "*Powered by OpenWeatherMap.org*\n"
            "Weather for {zip} ({city}):"
            "\n\n"
            "Currently {curtemp:.0f}°F with {condition} (feels like "
            "{feelslike:.0f}°F)."
            "\n\n"
            "Today is forecasted to have a high of {high:.0f}°F and a low of "
            "{low:.0f}°F, with {forecast}.".format(
                zip=zip,
                city=city,
                curtemp=float(current_weather["temp"]),
                condition=self.list_conditions(current_weather["weather"]),
                feelslike=float(current_weather["feels_like"]),
                high=float(daily_forecast["temp"]["max"]),
                low=float(daily_forecast["temp"]["min"]),
                forecast=self.list_conditions(daily_forecast["weather"])))

    def help_text(self):
        return (
            "```weather <zipCode>```"
            "Retrieves the current weather for the given zip code, as well as"
            " today's forecast.")

    async def run(self, command_io):
        zip_code_match = _zip_code_re.search(command_io.message.content)
        if not zip_code_match:
            raise ValueError
        async with command_io.message.channel.typing():
            zip_code = zip_code_match.group()
            worker = web_worker.WebWorker()
            # convert zip to lat/lon
            geocode = json.loads(
                worker.make_request(
                    "https://public.opendatasoft.com/api/records/1.0/search?"
                    "dataset=us-zip-code-latitude-and-longitude&q=zip={zip}".
                    format(zip=zip_code)))
            # fetch current & forecasted weather
            weather = json.loads(
                worker.make_request(
                    "https://api.openweathermap.org/data/2.5/onecall?"
                    "lat={lat}&lon={lon}&exclude=minutely,hourly&appid={key}&"
                    "units=imperial".format(lat=geocode["latitude"],
                                            lon=geocode["longitude"],
                                            key=self._api_key)))
            current_weather = weather["current"]
            daily_forecast = weather["daily"][0]
            response = self.build_message(zip_code, geocode["city"],
                                          current_weather, daily_forecast)
        await command_io.message.channel.send(response)
