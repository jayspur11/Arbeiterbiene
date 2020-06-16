""" This is the main file for the Discord bot. It's responsible for the primary
setup of the bot, as well as pulling in and configuring all the modules.
"""

import json
import logging
from discord.ext import commands

_bot = commands.Bot(None)
_command_registry = {}


@_bot.event
async def on_ready():
    print("Hello world!")


@_bot.event
async def on_message(message):
    if not (message.channel.is_private or _bot.user.id in message.raw_mentions):
        return
    content = message.content.split(' ', 2)
    cmd = content[1]
    if cmd not in _command_registry:
        # TODO: send an error message
        return
    command = _command_registry[cmd]
    try:
        await command.run(message, _bot)
    except (IndexError, ValueError):
        await _bot.send_message(message.channel, command.help_text())


def _configure_file_logging():
    """
    Configures the logging module to output logs to file ('discord.log').
    """
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8',
                                  mode='w')
    handler.setFormatter(
        logging.Formatter('%(asctime)s | %(levelname)s | %(name)s: %(message)s',
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
        print('Please set up an "auth.json" file in the same directory as '
              '"arbeiterbiene.py". It should follow the format of "example-auth'
              '.json".')
        return
    _bot.run(auth['token'])


if __name__ == '__main__':
    main()
