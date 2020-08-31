from commands.base_command import BaseCommand

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
        pass
