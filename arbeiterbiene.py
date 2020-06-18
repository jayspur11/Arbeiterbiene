""" This is the main file for the Discord bot. It's responsible for the primary
setup of the bot, as well as pulling in and configuring all the modules.
"""

import asyncio
import json
import logging
from commands import command_io
from commands import die_command
from commands import poll_command
from commands import repost_command
from commands import roll_command
from commands import scion_command
from discord.ext import commands

_event_loop = asyncio.get_event_loop()
_bot = commands.Bot("", loop=_event_loop)
_command_io = command_io.CommandIO(_bot, _event_loop)
_command_registry = {
    die_command.DieCommand.trigger_word(): die_command.DieCommand(),
    poll_command.PollCommand.trigger_word(): poll_command.PollCommand(),
    repost_command.RepostCommand.trigger_word(): repost_command.RepostCommand(),
    roll_command.RollCommand.trigger_word(): roll_command.RollCommand(),
    scion_command.ScionCommand.trigger_word(): scion_command.ScionCommand()
}


@_bot.event
async def on_ready():
    print("Hello world!")


@_bot.event
async def on_message(message):
    if not (type(message.channel) in ["DMChannel", "GroupChannel"]
            or _bot.user.id in message.raw_mentions):
        return
    content = message.content.split(' ', 2)
    cmd = content[1]
    message.content = content[2] if len(content) > 2 else ''
    if cmd not in _command_registry:
        # TODO: send an error message
        return
    command = _command_registry[cmd]
    _command_io.message = message
    try:
        await command.run(_command_io)
    except (IndexError, ValueError):
        await message.channel.send(command.help_text())


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
