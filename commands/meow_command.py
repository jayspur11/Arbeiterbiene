import json
from commands.base_command import BaseCommand
from urllib import request


class MeowCommand (BaseCommand):
    """Class to add a 'meow' command to the bot."""

    @classmethod
    def trigger_word(cls):
        return "meow"

    def help_text(self):
        return """```meow```
        Retrieves a random image of a cat, and a fun fact.
        """

    async def run(self, command_io):
        with request.urlopen("https://some-random-api.ml/facts/cat") as rfact, request.urlopen("https://some-random-api.ml/img/cat") as rimg:
            fact = json.loads(rfact.read())["fact"]
            img_url = json.loads(rimg.read())["link"]
            command_io.message.channel.send("%s\n%s" % fact, img_url)
