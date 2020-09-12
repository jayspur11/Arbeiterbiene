import json
import re
from commands.core.base_command import BaseCommand
from urllib import request

_zip_code_re = re.compile(r'\d{5}')


class AqiCommand(BaseCommand):
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

    async def run(self, command_io):
        if not len(command_io.message.content):
            raise ValueError
        zip_code_match = _zip_code_re.search(command_io.message.content)
        if not zip_code_match:
            raise ValueError
        req = request.Request(
            "https://airnowapi.org/aq/observation/zipCode/current"
            "?zipCode={zip_code}&format=application/json&api_key={api_key}"
            .format(zip_code=zip_code_match.group(), api_key=self._api_key))
        with request.urlopen(req) as raqi:
            results = json.loads(raqi.read().decode())
            message_list = [
                "Results for {zip}:".format(zip=zip_code_match.group())
            ]
            for result in results:
                message_list.append(
                    "AQI ({param}): {aqi} - {category}".format(
                        param=result.get('ParameterName', '{error}'),
                        aqi=result.get('AQI', '{error}'),
                        category=result.get('Category', {}).get('Name', '{error}')
                    )
                )
            await command_io.message.channel.send("\n".join(message_list))
