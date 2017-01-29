import asyncio
import json
import logging

## Module Setup
from modules import gaming

module_registry = {
    '$': gaming,
}

## Bot Setup
from discord.ext import commands

bot = commands.Bot(('BOT! ', '!'))
for trigger in module_registry:
    module_registry[trigger].bot = bot

## Bot Events
@bot.event
async def on_ready():
    print("Hello world!")

@bot.event
async def on_message(message):
    trigger = message.content[0]
    if trigger in module_registry:
        await module_registry[trigger].process_message(message)

## Bot Commands
@bot.command(pass_context=True)
async def echo(context):
    await bot.say(context.view.read_rest())

@bot.command(pass_context=True)
async def garble(context):
    await bot.say(transform(context.view.read_rest()))

@bot.command(pass_context=True)
async def ungarble(context):
    await bot.say(transform(context.view.read_rest()))

## Helper Functions
def transform(string):
    result = ""
    for char in string:
        if str.isalpha(char):
            result += chr((ord(char) ^ 31) - 4)
        else:
            result += char
    return result

## Misc Functions
def _configureFileLogging():
    '''
    Configures the logging module to output logs to file ('discord.log').
    '''
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8',
                                  mode='w')
    handler.setFormatter(
        logging.Formatter('%(asctime)s | %(levelname)s | %(name)s: %(message)s',
                          '%Y-%m-%d %I:%M:%S %p'))
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)


def main():
    '''
    The entry point of the Arbeiterbiene bot.
    '''
    _configureFileLogging()
    try:
        with open('auth.json', 'r') as authfile:
            auth = json.load(authfile)
    except FileNotFoundError:
        print('Please set up an "auth.json" file in the same directory as '
              '"arbeiterbiene.py". It should follow the format of "example-auth'
              '.json".')
        return
    bot.run(auth['token'])


if __name__=='__main__':
    main()
