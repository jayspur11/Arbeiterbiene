# TODO (jaysen): Document this file!

bot = None
module_commands = {}

def module_command(func):
    module_commands[func.__name__] = func

async def process_message(message):
    content = message.content.split(' ', 1)
    cmd = content[0][1:]
    message.content = content[1]
    if cmd in module_commands:
        await module_commands[cmd](message)
    else:
        raise KeyError
