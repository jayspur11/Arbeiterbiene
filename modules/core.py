'''
# core.py

Module for core bot commands.

A command belongs here if it...
 - is a tool for bot management, or
 - is generally useful.

A command does *not* belong here if it...
 - is a tool that isn't related to the bot, or
 - is a picture of Hitler.
'''

from modules import shared
from modules.module import *

## Commands
@module_command
async def die(message):
    '''```!die```
    Logs the bot out & kills the running process.
    '''
    await shared.bot.send_message(message.channel, ':(')
    raise KeyboardInterrupt

# TODO: Fix this one so it's not so dangerous.
#@module_command
async def echo(message):
    '''```!echo <msg>```
    Echoes the given message (`<msg>`) back to the server.
    
    **Notes:**
        Be careful with this one! Anyone can ask the bot to say *anything*,
        which is dangerous, because the bot might execute elevated commands.
    '''
    if not len(message.content):
        raise ValueError
    await shared.bot.send_message(message.channel, message.content)

# TODO: Fix this one so it's not so dangerous.
@module_command
async def garble(message):
    '''```!garble <msg>```
    Garbles the given message (`<msg>`) and echoes it back to the server.
    Also deletes the message that triggered the bot (but mentions the original
    sender).
    
    **Notes:**
     - This is a best-effort deal...if you see a `!garble` come in from
       someone, *don't read their message*!
     - On the same note, if you notice the bot doesn't garble your message, be
       kind and delete it.
    
    **See Also:** `ungarble`
    '''
    if not len(message.content):
        raise ValueError
    await shared.bot.delete_message(message)
    await shared.bot.send_message(
        message.channel,
        message.author.mention + ' ' + transform(message.content))

@module_command
async def ungarble(message):
    '''```!ungarble <msg>```
    Ungarbles the given message (`<msg>`) and PMs it back to the sender. Also
    deletes the message that triggered the bot (for cleanliness!).
    
    **See Also:** `garble`
    '''
    if not len(message.content):
        raise ValueError
    await shared.bot.delete_message(message)
    await shared.bot.send_message(message.author, transform(message.content))

## Helper Functions
def transform(string):
    result = ""
    for char in string:
        if str.isalpha(char):
            result += chr((ord(char) ^ 31) - 4)
        else:
            result += char
    return result
