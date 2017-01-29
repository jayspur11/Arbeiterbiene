# TODO (jaysen): Document this file!

bot = None
module_commands = {}

def module_command(func):
    '''
    Decorator to add a function as a command in the module.
    
    func (function):
        The function to be registered in the module. It must take 1 argument of
        type `discord.Message`.
        **Note:** `message.content` will have the command stripped from
        the front, leaving only the relevant pieces of the command in the
        string.
        
        The function name will be used to index the function. For example,
        decorating `def roll` will register the function under the `roll`
        command in the module.
    
    Usage:
        ```
        @module_command
        def <function_name>(message):
            ...
        ```
    '''
    module_commands[func.__name__] = func

async def process_message(message):
    content = message.content.split(' ', 1)
    cmd = content[0][1:]
    message.content = content[1]
    if cmd in module_commands:
        await module_commands[cmd](message)
    else:
        raise KeyError
