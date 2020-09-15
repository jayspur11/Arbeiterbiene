from commands.core import base_command
from commands.core import web_command
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

    def build_message(self, zip, curtemp, condition, feelslike, high, low,
                      forecast):
        """Build the message about weather to send to Discord.

        Args:
            zip (string): Zip code weather was requested for.
            curtemp (string): Current temperature (°F).
            condition (string): Current weather condition (e.g. sunny).
            feelslike (string): What the current temperature feels like (°F).
            high (string): Forecasted max temperature for the day (°F).
            low (string): Forecasted min temperature for the day (°F).
            forecast (string): Forecasted weather condition (e.g. sunny).

        Returns:
            string: Formatted message ready to send to Discord.
        """
        return (
            "Weather for {zip}:\n"
            "Currently {curtemp}°F with {condition} (feels like {feelslike}°F)."
            "\n\n"
            "Today is forecasted to have a high of {high}°F and a low of "
            "{low}°F, with {forecast}.".format(zip=zip,
                                               curtemp=curtemp,
                                               condition=condition,
                                               feelslike=feelslike,
                                               high=high,
                                               low=low,
                                               forecast=forecast))

    def help_text(self):
        return (
            "```weather <zipCode>```"
            "Retrieves the current weather for the given zip code, as well as"
            " today's forecast.")

    async def run(self, command_io):
        zip_code_match = _zip_code_re.search(command_io.message.content)
        if not zip_code_match:
            raise ValueError
        with command_io.message.channel.typing():
            zip_code = zip_code_match.group()
            # convert zip to lat/lon
            ods_req = web_command.WebCommandRequest(
                '', "https://public.opendatasoft.com/api/records/1.0/search?"
                "dataset=us-zip-code-latitude-and-longitude&q=zip={zip}".
                format(zip=zip_code))
            with request.urlopen(ods_req.request) as ods_res:
                geocode = json.loads(
                    ods_res.read().decode())["records"][0]["fields"]
            # fetch current & forecasted weather
            owm_req = web_command.WebCommandRequest(
                '', "https://api.openweathermap.org/data/2.5/onecall?"
                "lat={lat}&lon={lon}&exclude=minutely,hourly&appid={key}&"
                "units=imperial".format(lat=geocode["latitude"],
                                        lon=geocode["longitude"],
                                        key=self._api_key))
            with request.urlopen(owm_req.request) as owm_res:
                weather = json.loads(owm_res.read().decode())
            current_weather = weather["current"]
            daily_forecast = weather["daily"][0]
            response = self.build_message(
                zip_code, current_weather["temp"],
                current_weather["weather"]["description"],
                current_weather["feels_like"], daily_forecast["temp"]["max"],
                daily_forecast["temp"]["min"],
                daily_forecast["weather"]["description"])
        command_io.message.channel.send(response)
