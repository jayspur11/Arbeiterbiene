""" This is the main file for the Discord bot. It's responsible for the primary
setup of the bot, as well as pulling in and configuring all the modules.
"""
import commands
import json
import logging
import re
from discord.client import Client


class Arbeiterbiene(Client):
    _cmd_re = re.compile(r'(([^\s]+)\s*){2}(.*)')

    def __init__(self, airnowapi_key):
        super().__init__()
        self._command_registry = commands.command_registry(airnowapi_key)

    async def on_ready(self):
        print("Hello world!")

    async def on_message(self, message):
        if not (type(message.channel) in ["DMChannel", "GroupChannel"]
                or self.user.id in message.raw_mentions):
            return
        cmd, message.content = self._cmd_re.match(message.content).group(2, 3)
        cmd = cmd.lower()
        if cmd not in self._command_registry:
            # TODO: send an error message
            return
        command = self._command_registry[cmd]
        command_io = commands.CommandIO(message)
        try:
            await command.run(command_io)
        except (IndexError, ValueError, KeyError):
            await message.channel.send(command.help_text())


def _configure_file_logging():
    """
    Configures the logging module to output logs to file ('discord.log').
    """
    handler = logging.FileHandler(filename='discord.log',
                                  encoding='utf-8',
                                  mode='w')
    handler.setFormatter(
        logging.Formatter(
            '%(asctime)s | %(levelname)s | %(name)s: %(message)s',
            '%Y-%m-%d %I:%M:%S %p'))
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)


def main():
    """
    The entry point of the Arbeiterbiene bot.
    """
    _configure_file_logging()
    try:
        with open('auth.json', 'r') as authfile:
            auth = json.load(authfile)
    except FileNotFoundError:
        print(
            'Please set up an "auth.json" file in the same directory as '
            '"arbeiterbiene.py". It should follow the format of "example-auth'
            '.json".')
        return
    bot = Arbeiterbiene(auth.get('airnowapi_key', ''))
    bot.run(auth['token'])


if __name__ == '__main__':
    main()
