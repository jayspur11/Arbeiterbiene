'''
This file defines some syntactic sugar for creating modules!

To use it to define a module, import *everything*: `from .module import *`.
Then, just decorate your commands with `@module_command`.

To use a module defined this way, import the module as normal, then assign
`module.bot` to the discord.Bot instance and pass any commands to the module via
`module.process_message`.
'''

import discord

bot = None
module_commands = {}

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

async def process_message(message):
    '''
    Coroutine to process an incoming command for this module.
    
    message (discord.Message):
        The message received from the server.
    '''
    content = message.content.split(' ', 1)
    cmd = content[0][1:]
    message.content = content[1]
    if cmd in module_commands:
        await module_commands[cmd](message)
    else:
        raise KeyError
