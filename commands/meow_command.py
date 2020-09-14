import json

from commands.core import web_command
from discord import Embed
from urllib import request


class MeowCommand(web_command.WebCommand):
    """Class to add a 'meow' command to the bot."""
    @classmethod
    def trigger_word(cls):
        return "meow"

    def help_text(self):
        return """```meow```
        Retrieves a random image of a cat, and a fun fact.
        """

    def build_requests(self, command_io):
        return [
            web_command.WebCommandRequest(
                "fact", "https://some-random-api.ml/facts/cat"),
            web_command.WebCommandRequest(
                "image", "https://some-random-api.ml/img/cat")
        ]

    async def run(self, command_io):
        responses = self.fetch_web_responses(command_io)
        await command_io.message.channel.send(
            json.loads(responses["fact"])["fact"],
            embed=Embed().set_image(
                url=json.loads(responses["image"])["link"]))
