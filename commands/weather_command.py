from commands.core import web_command


class WeatherCommand(web_command.WebCommand):
    """Class to add 'weather' command to bot."""
    @classmethod
    def trigger_word(cls):
        return "weather"

    def __init__(self, api_key):
        """Prepare an instance to query `OpenWeatherMap.org`.

        api_key: (string) API key to use for OWM requests.
        """
        self._api_key = api_key

    def help_text(self):
        return (
            "```weather <zipCode>```"
            "Retrieves the current weather for the given zip code, as well as"
            " today's forecast.")

    def build_requests(self, command_io):
        pass

    async def run(self, command_io):
        raise ValueError
