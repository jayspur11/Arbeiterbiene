import asyncio
import discord
import json
import logging


def configureFileLogging():
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
    # Grab authentication info.
    try:
        with open('auth.json', 'r') as authfile:
            auth = json.load(authfile)
    except FileNotFoundError:
        print('Please set up an "auth.json" file in the same directory as '
              '"arbeiterbiene.py". It should follow the format of "example-auth'
              '.json".')
        return
    # Create bot client.
    client = discord.Client()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.login(auth['token']))
    # TODO: Something, now that we're logged in.
    loop.run_until_complete(client.logout())


if __name__=='__main__':
    main()
