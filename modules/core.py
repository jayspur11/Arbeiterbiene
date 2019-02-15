""" Module for core bot commands.

A command belongs here if it...
 - is a tool for bot management, or
 - is generally useful.

A command does *not* belong here if it...
 - is a tool that isn't related to the bot, or
 - is a picture of Hitler.
"""

from modules import module
from modules import shared


@module.module_command
async def die(message):
    """```die```
    Logs the bot out & kills the running process.
    """
    await shared.bot.send_message(message.channel, ':(')
    raise KeyboardInterrupt


# TODO: Fix this one so it's not so dangerous.
# @module.module_command
async def echo(message):
    """```echo <msg>```
    Echoes the given message (`<msg>`) back to the server.

    **Notes:**
        Be careful with this one! Anyone can ask the bot to say *anything*,
        which is dangerous, because the bot might execute elevated commands.
    """
    if not len(message.content):
        raise ValueError
    await shared.bot.send_message(message.channel, message.content)


@module.module_command
async def garble(message):
    """```garble <msg>```
    Garbles the given message (`<msg>`) and echoes it back to the server.
    Also deletes the message that triggered the bot (but mentions the original
    sender).

    **Notes:**
     - This is a best-effort deal...if you see a `!garble` come in from
       someone, *don't read their message*!
     - On the same note, if you notice the bot doesn't garble your message, be
       kind and delete it.

    **See Also:** `ungarble`
    """
    if not len(message.content):
        raise ValueError
    await shared.bot.delete_message(message)
    await shared.bot.send_message(
        message.channel,
        message.author.mention + ' ' + _transform(message.content))


@module.module_command
async def help(message):
    """```help [<command>]```
    Prints a help message.

    `help` by itself will print the available commands.

    `help <command>` will print that specific command's documentation.
    """
    docs = []
    if not len(message.content):
        docs += list('Available commands:')
        for command in module.module_commands:
            docs += list(' ' + command + ',')
        docs[-1] = '.'
    await shared.bot.send_message(message.author, ''.join(docs))


@module.module_command
async def ungarble(message):
    """```ungarble <msg>```
    Ungarbles the given message (`<msg>`) and PMs it back to the sender. Also
    deletes the message that triggered the bot (for cleanliness!).
    
    **See Also:** `garble`
    """
    if not len(message.content):
        raise ValueError
    await shared.bot.delete_message(message)
    await shared.bot.send_message(message.author, _transform(message.content))


def _transform(string):
    result = ""
    for char in string:
        if str.isalpha(char):
            result += chr((ord(char) ^ 31) - 4)
        else:
            result += char
    return result
