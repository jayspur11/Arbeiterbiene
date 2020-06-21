import json
from commands import BaseCommand
from discord import Embed
from urllib import request


class WoofCommand(BaseCommand):
    """Class to add a 'woof' command to the bot."""

    @classmethod
    def trigger_word(cls):
        return "woof"

    def help_text(self):
        return """```woof```
        Retrieves a random image of a dog, and a fun fact.
        """

    async def run(self, command_io):
        freq = request.Request("https://some-random-api.ml/facts/dog", headers={"User-Agent": "arbeiterbiene"})
        ireq = request.Request("http://some-random-api.ml/img/dog", headers={"User-Agent": "arbeiterbiene"})
        with request.urlopen(freq) as rfact, request.urlopen(ireq) as rimg:
            fact = json.loads(rfact.read())["fact"]
            img_url = json.loads(rimg.read())["link"]
            await command_io.message.channel.send(fact, embed=Embed().set_image(url=img_url))
