from commands.base_command import BaseCommand

class AqiCommand(BaseCommand):
    """Class to add 'aqi' command to bot."""

    @classmethod
    def trigger_word(cls):
        return "aqi"

    def help_text(self):
        return """```aqi <zipCode>```
        Retrieves the current Air Quality Index for the given zip code.
        """

    async def run(self, command_io):
        pass
