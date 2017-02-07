'''
# module.py

This file defines some syntactic sugar for creating modules!

To use it to define a module, import *everything*:
`from modules.module import *`.
Then, just decorate your commands with `@module_command`.

To use a module defined this way, import the module as normal, then pass any
commands to the module via `module.process_message`.
**Note:** You'll need to configure the global variables in `shared.py`.
'''

from modules import shared
import discord

## Module Setup
# To be filled in by the inheriting module.

module_commands = {}
module_description = ''
module_name = ''

def module_command(func):
    '''
    Decorator to add a function as a command in the module.
    
    func (function):
        The function to be registered in the module. It must be `async` and take
        1 argument of type `discord.Message`.
        **Note:** `message.content` will have the command stripped from
        the front, leaving only the relevant pieces of the command in the
        string.
        
        The function name will be used to index the function. For example,
        decorating `def roll` will register the function under the `roll`
        command in the module.
    
    Usage:
        ```
        @module_command
        async def <function_name>(message):
            ...
        ```
    '''
    module_commands[func.__name__] = func

## Module-level Functions
async def process_message(message):
    '''
    Coroutine to process an incoming command for this module.
    
    message (discord.Message):
        The message received from the server.
    '''
    content = message.content.split(' ', 1)
    cmd = content[0][1:]
    if cmd in module_commands:
        func = module_commands[cmd]
        try:
            message.content = content[1] if len(content) > 1 else ''
            await func(message)
        except (IndexError, ValueError):
            await shared.bot.send_message(message.channel, func.__doc__)
            pass
    else:
        raise KeyError
