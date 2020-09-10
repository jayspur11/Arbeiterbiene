""" This is the main file for the Discord bot. It's responsible for the primary
setup of the bot, as well as pulling in and configuring all the modules.
"""
import asyncio
import commands
import json
import logging
import re
from discord.ext import commands as discord_commands

_event_loop = asyncio.get_event_loop()
_bot = discord_commands.Bot("", loop=_event_loop)
_cmd_re = re.compile(r'(([^\s]+)\s*){2}(.*)')


@_bot.event
async def on_ready():
    print("Hello world!")


@_bot.event
async def on_message(message):
    if not (type(message.channel) in ["DMChannel", "GroupChannel"]
            or _bot.user.id in message.raw_mentions):
        return
    cmd, message.content = _cmd_re.match(message.content).group(2,3)
    cmd = cmd.lower()
    if cmd not in _command_registry:
        # TODO: send an error message
        return
    command = _command_registry[cmd]
    command_io = commands.CommandIO(_bot, _event_loop, message)
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
    global _command_registry
    _configure_file_logging()
    try:
        with open('auth.json', 'r') as authfile:
            auth = json.load(authfile)
            _command_registry = commands.command_registry(
                auth.get('airnowapi_key', ''))
    except FileNotFoundError:
        print(
            'Please set up an "auth.json" file in the same directory as '
            '"arbeiterbiene.py". It should follow the format of "example-auth'
            '.json".')
        return
    _bot.run(auth['token'])


if __name__ == '__main__':
    main()
