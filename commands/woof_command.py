import discord
import json

from commands.core import web_command
from urllib import request


class WoofCommand(web_command.WebCommand):
    """Class to add a 'woof' command to the bot."""
    @classmethod
    def trigger_word(cls):
        return "woof"

    def help_text(self):
        return """```woof```
        Retrieves a random image of a dog, and a fun fact.
        """

    def build_requests(self, command_io):
        return [
            web_command.WebCommandRequest(
                "fact", "https://some-random-api.ml/facts/dog"),
            web_command.WebCommandRequest(
                "image", "https://some-random-api.ml/img/dog")
        ]

    async def run(self, command_io):
        responses = self.fetch_web_responses(command_io)
        await command_io.message.channel.send(
            json.loads(responses["fact"])["fact"],
            embed=discord.Embed().set_image(
                url=json.loads(responses["image"])["link"]))
