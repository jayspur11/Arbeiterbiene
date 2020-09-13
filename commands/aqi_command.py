import json
import re

from commands.core import web_command
from urllib import request

_zip_code_re = re.compile(r'\d{5}')


class AqiCommand(web_command.WebCommand):
    """Class to add 'aqi' command to bot."""
    @classmethod
    def trigger_word(cls):
        return "aqi"

    def __init__(self, api_key):
        """Prepare an instance to query `AirNowApi.org`.

        api_key: (string) API key to use for the AirNowApi requests.
        """
        self._api_key = api_key

    def help_text(self):
        return """```aqi <zipCode>```
        Retrieves the current Air Quality Index for the given zip code.
        """

    def build_aqi_message(self, aqi):
        return "AQI ({param}): {aqi} - {category}".format(
            param=aqi.get("ParameterName", "ERROR"),
            aqi=aqi.get("AQI", "ERROR"),
            category=aqi.get("Category", {}).get("Name", "ERROR"))

    def build_requests(self, command_io):
        zip_code_match = _zip_code_re.search(command_io.message.content)
        if not zip_code_match:
            raise ValueError
        return [
            web_command.WebCommandRequest(
                "aqi", "https://airnowapi.org/aq/observation/zipCode/current"
                "?zipCode={zip_code}&format=application/json&api_key={api_key}"
                .format(zip_code=zip_code_match.group(),
                        api_key=self._api_key))
        ]

    async def run(self, command_io):
        web_responses = self.fetch_web_responses(command_io)
        results = json.loads(web_responses["aqi"])
        message_list = [self.build_aqi_message(result) for result in results]
        await command_io.message.channel.send("\n".join(message_list))
