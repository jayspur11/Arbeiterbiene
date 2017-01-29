# TODO (jaysen): Document this file!

module_commands = {}

def module_command(*args, **kwargs):
    def decorator(func):
        module_commands[func.__name__] = func
    return decorator

def process_message(message):
    cmd = message.content.split(' ', 1)[0][1:]
    if cmd in module_commands:
        module_commands[cmd](message)
    else:
        raise KeyError
