""" This is the main file for the Discord bot. It's responsible for the primary
setup of the bot, as well as pulling in and configuring all the modules.
"""

from discord.ext import commands
from modules import community
from modules import core
from modules import gaming
from modules import module
from modules import shared
import json
import logging

shared.bot = commands.Bot(None)
community.register_commands()
core.register_commands()
gaming.register_commands()


@shared.bot.event
async def on_ready():
    print("Hello world!")


@shared.bot.event
async def on_message(message):
    if message.channel.is_private or shared.bot.user.id in message.raw_mentions:
        await module.process_message(message)


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
    shared.bot.run(auth['token'])


if __name__ == '__main__':
    main()
