from commands.core import base_command
from urllib import request


class WebCommandRequest:
    def __init__(self, identifier, url, headers={}):
        self.identifier = identifier
        self.request = request.Request(
            url, headers={'User-Agent': 'arbeiterbiene', **headers})


class WebCommand(base_command.BaseCommand):
    """Base class for commands that fetch information from the web."""
    async def fetch_web_responses(self, command_io):
        results = {}
        async with command_io.message.channel.typing():
            for cmd_request in self.build_requests(command_io):
                with request.urlopen(cmd_request.request) as req:
                    results[cmd_request.identifier] = req.read()
        return results

    def build_requests(self, command_io):
        raise NotImplementedError
