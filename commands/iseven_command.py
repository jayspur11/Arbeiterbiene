import json
import re

from commands.core import web_command

_number_re = re.compile(r'\b\d+\b')


class IsevenCommand(web_command.WebCommand):
    """Class to add 'isEven' command to bot."""
    @classmethod
    def trigger_word(cls):
        return "iseven"

    def help_text(self):
        return """```iseven <number>```
        Retrieves whether the given number is even. (ad-supported)
        """

    def build_requests(self, command_io):
        num_match = _number_re.search(command_io.message.content)
        if not num_match:
            raise ValueError
        return [
            web_command.WebCommandRequest(
                "iseven",
                f"https://api.isevenapi.xyz/api/iseven/{num_match.group()}")
        ]
        
    async def run(self, command_io):
        web_responses = self.fetch_web_responses(command_io)
        results = json.loads(web_responses["iseven"])
        num_match = _number_re.search(command_io.message.content)
        if "error" in results:
            message = "Number not in range [0, 999999]"
        else:
            evenness = "is" if results["iseven"] else "is not"
            message = (
                f"{num_match.group()} {evenness} even.\n" +
                f"*Brought to you by:*\n```{results['ad']}```")
        await command_io.message.channel.send(message)
